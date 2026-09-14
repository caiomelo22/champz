import typing as t
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.users import current_active_user
from app.db.base import get_async_session
from app.dependencies.championship import get_championship_access, require_owner
from app.models_orm.bid import Bid
from app.models_orm.player_auction import PlayerAuction
from app.models_orm.user import User
from app.services.auction import (
    cancel_auction,
    configure_auctions,
    finalize_due_auctions,
    place_bid,
    update_auction,
)


router = APIRouter()


class ConfigureAuctionsModel(BaseModel):
    player_ids: list[str] = Field(min_length=1)
    deadline: datetime
    minimum_bid: int = Field(gt=0)


class UpdateAuctionModel(BaseModel):
    deadline: datetime
    minimum_bid: int = Field(gt=0)


class PlaceBidModel(BaseModel):
    amount: int = Field(gt=0)
    participant_id: t.Optional[int] = None


class AuctionResponse(BaseModel):
    id: int
    player_id: str
    player_name: str
    deadline: datetime
    minimum_bid: int
    status: str
    leading_participant_id: t.Optional[int] = None
    leading_participant_name: t.Optional[str] = None
    leading_bid: t.Optional[int] = None
    bid_count: int = 0
    is_current_user_leader: bool = False


class BidResultResponse(BaseModel):
    auction: AuctionResponse
    available_budget: int


async def _auction_response(
    session: AsyncSession,
    auction: PlayerAuction,
    current_participant_id: t.Optional[int],
    known_bid_count: t.Optional[int] = None,
) -> AuctionResponse:
    bid_count = known_bid_count
    if bid_count is None:
        bid_count = (
            await session.execute(select(func.count(Bid.id)).where(Bid.auction_id == auction.id))
        ).scalar_one()
    return AuctionResponse(
        id=auction.id,
        player_id=auction.player_id,
        player_name=auction.player.name,
        deadline=auction.deadline.replace(tzinfo=timezone.utc),
        minimum_bid=auction.minimum_bid,
        status=auction.status,
        leading_participant_id=auction.leading_participant_id,
        leading_participant_name=(
            auction.leading_participant.name if auction.leading_participant else None
        ),
        leading_bid=auction.leading_bid,
        bid_count=bid_count,
        is_current_user_leader=auction.leading_participant_id == current_participant_id,
    )


async def _load_auction(session: AsyncSession, championship_id: int, auction_id: int) -> PlayerAuction:
    return (
        await session.execute(
            select(PlayerAuction)
            .where(
                PlayerAuction.id == auction_id,
                PlayerAuction.championship_id == championship_id,
            )
            .options(
                selectinload(PlayerAuction.player),
                selectinload(PlayerAuction.leading_participant),
            )
        )
    ).scalar_one()


@router.get("/{championship_id}/auction/list", response_model=list[AuctionResponse])
async def list_auctions(
    championship_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    await finalize_due_auctions(championship_id)
    access = await get_championship_access(session, championship_id, user)
    auctions = (
        await session.execute(
            select(PlayerAuction)
            .where(PlayerAuction.championship_id == championship_id)
            .options(
                selectinload(PlayerAuction.player),
                selectinload(PlayerAuction.leading_participant),
            )
            .order_by(PlayerAuction.deadline, PlayerAuction.id)
        )
    ).scalars().all()
    auction_ids = [auction.id for auction in auctions]
    bid_counts = {}
    if auction_ids:
        bid_counts = dict(
            (
                await session.execute(
                    select(Bid.auction_id, func.count(Bid.id))
                    .where(Bid.auction_id.in_(auction_ids))
                    .group_by(Bid.auction_id)
                )
            ).all()
        )
    participant_id = access.participant.id if access.participant else None
    return [
        await _auction_response(
            session,
            auction,
            participant_id,
            known_bid_count=bid_counts.get(auction.id, 0),
        )
        for auction in auctions
    ]


@router.post("/{championship_id}/auction/configure", response_model=list[AuctionResponse])
async def configure_auction_batch(
    championship_id: int,
    data: ConfigureAuctionsModel,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    access = await get_championship_access(session, championship_id, user)
    require_owner(access)
    auctions = await configure_auctions(
        session,
        championship_id,
        data.player_ids,
        data.deadline,
        data.minimum_bid,
    )
    loaded = [await _load_auction(session, championship_id, auction.id) for auction in auctions]
    participant_id = access.participant.id if access.participant else None
    return [await _auction_response(session, auction, participant_id) for auction in loaded]


@router.patch("/{championship_id}/auction/{auction_id}", response_model=AuctionResponse)
async def edit_auction(
    championship_id: int,
    auction_id: int,
    data: UpdateAuctionModel,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    access = await get_championship_access(session, championship_id, user)
    require_owner(access)
    await update_auction(
        session,
        championship_id,
        auction_id,
        data.deadline,
        data.minimum_bid,
    )
    auction = await _load_auction(session, championship_id, auction_id)
    participant_id = access.participant.id if access.participant else None
    return await _auction_response(session, auction, participant_id)


@router.delete("/{championship_id}/auction/{auction_id}", response_model=AuctionResponse)
async def remove_auction(
    championship_id: int,
    auction_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    access = await get_championship_access(session, championship_id, user)
    require_owner(access)
    await cancel_auction(session, championship_id, auction_id)
    auction = await _load_auction(session, championship_id, auction_id)
    participant_id = access.participant.id if access.participant else None
    return await _auction_response(session, auction, participant_id)


@router.post("/{championship_id}/auction/{auction_id}/bid", response_model=BidResultResponse)
async def submit_bid(
    championship_id: int,
    auction_id: int,
    data: PlaceBidModel,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    access = await get_championship_access(session, championship_id, user)
    if access.role == "owner":
        bidder_participant_id = data.participant_id or (
            access.participant.id if access.participant else None
        )
        if bidder_participant_id is None:
            raise HTTPException(status_code=400, detail="Select a participant to place the bid.")
    elif user.is_verified and access.participant:
        if data.participant_id is not None and data.participant_id != access.participant.id:
            raise HTTPException(status_code=403, detail="Participants can only bid for themselves.")
        bidder_participant_id = access.participant.id
    else:
        raise HTTPException(status_code=403, detail="A verified linked participant is required to bid.")

    _, participant = await place_bid(
        session,
        championship_id,
        auction_id,
        user.id,
        data.amount,
        bidder_participant_id=bidder_participant_id,
    )
    auction = await _load_auction(session, championship_id, auction_id)
    return BidResultResponse(
        auction=await _auction_response(session, auction, participant.id),
        available_budget=participant.budget,
    )