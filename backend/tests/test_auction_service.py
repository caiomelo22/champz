from datetime import timedelta, timezone

import pytest
from fastapi import HTTPException
from sqlalchemy import func, select

from app.models_orm.bid import Bid
from app.models_orm.draft_pick import DraftPick
from app.routers.v2.participant import ManageParticipantModel, update_participant
from app.routers.v2.player import BuyPlayerModel, buy_player
from app.services.auction import cancel_auction, close_auction, normalize_deadline, place_bid, utc_now


async def test_outbid_refunds_previous_leader_and_debits_new_leader(session, auction_setup):
    data = auction_setup

    await place_bid(
        session,
        data["championship"].id,
        data["auction"].id,
        data["first_user"].id,
        20,
    )
    assert data["first_participant"].budget == 80

    await place_bid(
        session,
        data["championship"].id,
        data["auction"].id,
        data["first_user"].id,
        25,
    )
    assert data["first_participant"].budget == 75

    auction, second_participant = await place_bid(
        session,
        data["championship"].id,
        data["auction"].id,
        data["second_user"].id,
        30,
    )

    assert data["first_participant"].budget == 100
    assert second_participant.budget == 70
    assert auction.leading_participant_id == second_participant.id
    assert auction.leading_bid == 30
    assert (
        await session.execute(select(func.count(Bid.id)).where(Bid.auction_id == auction.id))
    ).scalar_one() == 3


async def test_close_auction_creates_one_pick_without_second_debit(session, auction_setup):
    data = auction_setup
    auction, participant = await place_bid(
        session,
        data["championship"].id,
        data["auction"].id,
        data["first_user"].id,
        40,
    )
    auction.deadline = utc_now() - timedelta(minutes=1)
    await session.commit()

    assert await close_auction(session, data["championship"].id, auction.id) is True
    assert await close_auction(session, data["championship"].id, auction.id) is False

    pick = (
        await session.execute(select(DraftPick).where(DraftPick.championship_id == data["championship"].id))
    ).scalar_one()
    assert pick.participant_id == participant.id
    assert pick.player_id == auction.player_id
    assert pick.value == 40
    assert participant.budget == 60


def test_deadline_is_normalized_to_utc_minute():
    deadline = utc_now().replace(tzinfo=timezone.utc) + timedelta(hours=1, seconds=37, microseconds=12)
    normalized = normalize_deadline(deadline)

    assert normalized.tzinfo is None
    assert normalized.second == 0
    assert normalized.microsecond == 0


async def test_bid_must_meet_minimum_and_available_budget(session, auction_setup):
    data = auction_setup

    with pytest.raises(HTTPException, match="Bid must be at least"):
        await place_bid(
            session,
            data["championship"].id,
            data["auction"].id,
            data["first_user"].id,
            9,
        )

    with pytest.raises(HTTPException, match="does not have enough budget"):
        await place_bid(
            session,
            data["championship"].id,
            data["auction"].id,
            data["first_user"].id,
            101,
        )

    assert data["first_participant"].budget == 100


async def test_cancel_auction_refunds_current_leader(session, auction_setup):
    data = auction_setup
    auction, participant = await place_bid(
        session,
        data["championship"].id,
        data["auction"].id,
        data["first_user"].id,
        35,
    )
    assert participant.budget == 65

    cancelled = await cancel_auction(session, data["championship"].id, auction.id)

    assert cancelled.status == "cancelled"
    assert participant.budget == 100
    assert (
        await session.execute(select(func.count(DraftPick.id)))
    ).scalar_one() == 0


async def test_participant_budget_cannot_change_while_leading(session, auction_setup):
    data = auction_setup
    await place_bid(
        session,
        data["championship"].id,
        data["auction"].id,
        data["first_user"].id,
        35,
    )

    with pytest.raises(HTTPException, match="Budget cannot be changed"):
        await update_participant(
            data["championship"].id,
            data["first_participant"].id,
            ManageParticipantModel(team="Test FC", name="First", budget=100),
            data["first_user"],
            session,
        )

    assert data["first_participant"].budget == 65


async def test_player_with_open_auction_cannot_be_assigned_manually(session, auction_setup):
    data = auction_setup

    with pytest.raises(HTTPException, match="cannot be assigned manually"):
        await buy_player(
            data["championship"].id,
            data["auction"].player_id,
            BuyPlayerModel(participant_id=data["first_participant"].id, value=20),
            data["first_user"],
            session,
        )