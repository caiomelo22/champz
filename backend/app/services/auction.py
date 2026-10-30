from datetime import datetime, timezone
from typing import Iterable, Optional
import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import async_session_maker
from app.models_orm.bid import Bid
from app.models_orm.championship import Championship
from app.models_orm.draft_pick import DraftPick
from app.models_orm.participant import Participant
from app.models_orm.player import Player
from app.models_orm.player_auction import PlayerAuction
from app.services.draft_pool import ensure_in_pool


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def normalize_deadline(deadline: datetime) -> datetime:
    if deadline.tzinfo is not None:
        deadline = deadline.astimezone(timezone.utc).replace(tzinfo=None)
    return deadline.replace(second=0, microsecond=0)


async def configure_auctions(
    session: AsyncSession,
    championship_id: int,
    player_ids: Iterable[str],
    deadline: datetime,
    minimum_bid: int,
) -> list[PlayerAuction]:
    normalized_player_ids = list(dict.fromkeys(player_ids))
    normalized_deadline = normalize_deadline(deadline)
    if not normalized_player_ids:
        raise HTTPException(status_code=400, detail="At least one player is required.")
    if normalized_deadline <= utc_now():
        raise HTTPException(status_code=400, detail="Deadline must be in the future.")
    if minimum_bid <= 0:
        raise HTTPException(status_code=400, detail="Minimum bid must be greater than zero.")

    championship = (
        await session.execute(
            select(Championship)
            .where(Championship.id == championship_id)
            .with_for_update()
        )
    ).scalar_one()
    if championship.status != "draft":
        raise HTTPException(status_code=409, detail="Auctions are only available during the draft.")

    existing_players = set(
        (
            await session.execute(
                select(Player.id).where(Player.id.in_(normalized_player_ids))
            )
        ).scalars().all()
    )
    if existing_players != set(normalized_player_ids):
        raise HTTPException(status_code=404, detail="One or more players were not found.")
    await ensure_in_pool(session, championship_id, normalized_player_ids)

    existing_pick = (
        await session.execute(
            select(DraftPick.id).where(
                DraftPick.championship_id == championship_id,
                DraftPick.player_id.in_(normalized_player_ids),
            ).limit(1)
        )
    ).scalar_one_or_none()
    if existing_pick:
        raise HTTPException(status_code=409, detail="A selected player has already been drafted.")

    existing_auctions = (
        await session.execute(
            select(PlayerAuction).where(
                PlayerAuction.championship_id == championship_id,
                PlayerAuction.player_id.in_(normalized_player_ids),
            ).order_by(PlayerAuction.id).with_for_update()
        )
    ).scalars().all()
    if any(auction.status != "cancelled" for auction in existing_auctions):
        raise HTTPException(status_code=409, detail="A selected player already has an auction.")

    auctions_by_player = {auction.player_id: auction for auction in existing_auctions}
    auctions = []
    for player_id in normalized_player_ids:
        auction = auctions_by_player.get(player_id)
        if auction is None:
            auction = PlayerAuction(championship_id=championship_id, player_id=player_id)
        auction.deadline = normalized_deadline
        auction.minimum_bid = minimum_bid
        auction.status = "open"
        auction.leading_participant_id = None
        auction.leading_participant = None
        auction.leading_bid = None
        auctions.append(auction)
    session.add_all(auctions)
    await session.commit()
    return auctions


async def update_auction(
    session: AsyncSession,
    championship_id: int,
    auction_id: int,
    deadline: datetime,
    minimum_bid: int,
) -> PlayerAuction:
    # Use the same lock order as batch configuration and manual assignment.
    championship = (
        await session.execute(
            select(Championship)
            .where(Championship.id == championship_id)
            .with_for_update()
        )
    ).scalar_one()
    auction = await _locked_auction(session, championship_id, auction_id)
    if auction.status not in {"open", "cancelled"}:
        raise HTTPException(status_code=409, detail="Only open or cancelled auctions can be updated.")
    restarting = auction.status == "cancelled"
    if restarting:
        if championship.status != "draft":
            raise HTTPException(status_code=409, detail="Auctions are only available during the draft.")
        existing_pick = (
            await session.execute(
                select(DraftPick.id).where(
                    DraftPick.championship_id == championship_id,
                    DraftPick.player_id == auction.player_id,
                ).limit(1)
            )
        ).scalar_one_or_none()
        if existing_pick is not None:
            raise HTTPException(status_code=409, detail="This player has already been drafted.")
    if not restarting and auction.deadline <= utc_now():
        await _close_locked_auction(session, auction)
        await session.commit()
        raise HTTPException(status_code=409, detail="Auction deadline has passed.")
    if not restarting and auction.leading_participant_id is not None:
        raise HTTPException(status_code=409, detail="An auction with bids cannot be edited.")

    normalized_deadline = normalize_deadline(deadline)
    if normalized_deadline <= utc_now():
        raise HTTPException(status_code=400, detail="Deadline must be in the future.")
    if minimum_bid <= 0:
        raise HTTPException(status_code=400, detail="Minimum bid must be greater than zero.")

    auction.deadline = normalized_deadline
    auction.minimum_bid = minimum_bid
    if restarting:
        auction.status = "open"
        auction.leading_participant_id = None
        auction.leading_participant = None
        auction.leading_bid = None
    await session.commit()
    return auction


async def place_bid(
    session: AsyncSession,
    championship_id: int,
    auction_id: int,
    user_id: uuid.UUID,
    amount: int,
    bidder_participant_id: Optional[int] = None,
) -> tuple[PlayerAuction, Participant]:
    auction = await _locked_auction(session, championship_id, auction_id)
    if auction.status != "open":
        raise HTTPException(status_code=409, detail="Auction is not open.")
    if auction.deadline <= utc_now():
        await _close_locked_auction(session, auction)
        await session.commit()
        raise HTTPException(status_code=409, detail="Auction deadline has passed.")

    bidder_query = select(Participant.id).where(
        Participant.championship_id == championship_id,
    )
    if bidder_participant_id is not None:
        bidder_query = bidder_query.where(Participant.id == bidder_participant_id)
    else:
        bidder_query = bidder_query.where(Participant.user_id == user_id)
    bidder_id = (await session.execute(bidder_query)).scalar_one_or_none()
    if bidder_id is None:
        raise HTTPException(status_code=403, detail="A valid participant is required to bid.")

    participant_ids = {bidder_id}
    if auction.leading_participant_id is not None:
        participant_ids.add(auction.leading_participant_id)
    locked_participants = (
        await session.execute(
            select(Participant)
            .where(Participant.id.in_(sorted(participant_ids)))
            .order_by(Participant.id)
            .with_for_update()
        )
    ).scalars().all()
    participant_by_id = {participant.id: participant for participant in locked_participants}
    bidder = participant_by_id[bidder_id]

    minimum_amount = auction.minimum_bid if auction.leading_bid is None else auction.leading_bid + 1
    if amount < minimum_amount:
        raise HTTPException(
            status_code=400,
            detail=f"Bid must be at least {minimum_amount}.",
        )

    if auction.leading_participant_id == bidder.id:
        debit = amount - (auction.leading_bid or 0)
    else:
        debit = amount

    if bidder.budget < debit:
        raise HTTPException(status_code=400, detail="Participant does not have enough budget.")

    if auction.leading_participant_id is not None and auction.leading_participant_id != bidder.id:
        previous_leader = participant_by_id[auction.leading_participant_id]
        previous_leader.budget += auction.leading_bid or 0

    bidder.budget -= debit
    auction.leading_participant_id = bidder.id
    auction.leading_bid = amount
    session.add(Bid(auction_id=auction.id, participant_id=bidder.id, amount=amount))
    await session.commit()
    return auction, bidder


async def cancel_auction(
    session: AsyncSession,
    championship_id: int,
    auction_id: int,
) -> PlayerAuction:
    auction = await _locked_auction(session, championship_id, auction_id)
    if auction.status != "open":
        raise HTTPException(status_code=409, detail="Only open auctions can be cancelled.")
    if auction.deadline <= utc_now():
        await _close_locked_auction(session, auction)
        await session.commit()
        raise HTTPException(status_code=409, detail="Auction deadline has passed.")

    if auction.leading_participant_id is not None:
        leader = (
            await session.execute(
                select(Participant)
                .where(Participant.id == auction.leading_participant_id)
                .with_for_update()
            )
        ).scalar_one()
        leader.budget += auction.leading_bid or 0

    auction.status = "cancelled"
    await session.commit()
    return auction


async def close_auction(
    session: AsyncSession,
    championship_id: int,
    auction_id: int,
) -> bool:
    auction = await _locked_auction(session, championship_id, auction_id)
    if auction.status != "open" or auction.deadline > utc_now():
        await session.commit()
        return False

    await _close_locked_auction(session, auction)
    await session.commit()
    return True


async def finalize_due_auctions(
    championship_id: Optional[int] = None,
    limit: int = 100,
) -> int:
    async with async_session_maker() as lookup_session:
        statement = (
            select(PlayerAuction.id, PlayerAuction.championship_id)
            .where(
                PlayerAuction.status == "open",
                PlayerAuction.deadline <= utc_now(),
            )
            .order_by(PlayerAuction.deadline, PlayerAuction.id)
            .limit(limit)
        )
        if championship_id is not None:
            statement = statement.where(PlayerAuction.championship_id == championship_id)
        due_auctions = (await lookup_session.execute(statement)).all()

    closed_count = 0
    for auction_id, due_championship_id in due_auctions:
        async with async_session_maker() as session:
            if await close_auction(session, due_championship_id, auction_id):
                closed_count += 1
    return closed_count


async def _locked_auction(
    session: AsyncSession,
    championship_id: int,
    auction_id: int,
) -> PlayerAuction:
    auction = (
        await session.execute(
            select(PlayerAuction)
            .where(
                PlayerAuction.id == auction_id,
                PlayerAuction.championship_id == championship_id,
            )
            .with_for_update()
        )
    ).scalar_one_or_none()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found.")
    return auction


async def _close_locked_auction(session: AsyncSession, auction: PlayerAuction) -> None:
    if auction.status != "open":
        return
    if auction.leading_participant_id is not None and auction.leading_bid is not None:
        session.add(
            DraftPick(
                championship_id=auction.championship_id,
                participant_id=auction.leading_participant_id,
                player_id=auction.player_id,
                value=auction.leading_bid,
            )
        )
    auction.status = "closed"