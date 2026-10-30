from datetime import timedelta

import pytest
from fastapi import HTTPException

from app.models.championship import CreateChampionshipModel
from app.models.player import BuyPlayerModel, UpdatePoolModel
from app.models_orm.draft_pick import DraftPick
from app.models_orm.player import Player
from app.routers.championship import create_championship
from app.routers.v2.player import (
    buy_player,
    get_player_pool,
    list_players,
    player_catalog,
    update_player_pool,
)
from app.services.auction import cancel_auction, configure_auctions, utc_now
from app.services.draft_pool import get_pool_player_ids


async def _add_players(session, source_id, overalls):
    source = await session.get(Player, source_id)
    players = [
        Player(**{
            column.name: getattr(source, column.name)
            for column in Player.__table__.columns
            if column.name not in ('id', 'overall')
        }, id=f'player-{overall}', overall=overall)
        for overall in overalls
    ]
    session.add_all(players)
    await session.commit()
    return players


async def test_catalog_selects_top_players_by_position(session, auction_setup):
    data = auction_setup
    await _add_players(session, data['auction'].player_id, [90, 85, 70])

    # Attackers: 2 per participant, the fixture player has overall 80
    catalog = await player_catalog(1, data['first_user'], session)

    assert {p.id for p in catalog if p.selected} == {'player-90', 'player-85'}
    assert len(catalog) == 4
    assert not any(p.locked for p in catalog)


async def test_create_championship_stores_selected_pool(session, auction_setup):
    data = auction_setup
    await _add_players(session, data['auction'].player_id, [90, 85])

    created = await create_championship(
        CreateChampionshipModel(name='New', player_ids=['player-90']), data['first_user'], session,
    )

    assert await get_pool_player_ids(session, created.id) == {'player-90'}
    listed = await list_players(created.id, None, None, data['first_user'], session)
    assert [p.id for p in listed] == ['player-90']


async def test_create_championship_rejects_unknown_players(session, auction_setup):
    with pytest.raises(HTTPException, match='not found'):
        await create_championship(
            CreateChampionshipModel(name='New', player_ids=['missing']), auction_setup['first_user'], session,
        )


async def test_player_with_open_auction_cannot_leave_pool(session, auction_setup):
    data = auction_setup

    with pytest.raises(HTTPException, match='cannot be removed'):
        await update_player_pool(data['championship'].id, UpdatePoolModel(player_ids=[]), data['first_user'], session)


async def test_drafted_player_cannot_leave_pool(session, auction_setup):
    data = auction_setup
    [player] = await _add_players(session, data['auction'].player_id, [90])
    await update_player_pool(
        data['championship'].id,
        UpdatePoolModel(player_ids=[data['auction'].player_id, player.id]),
        data['first_user'], session,
    )
    await buy_player(
        data['championship'].id, player.id,
        BuyPlayerModel(participant_id=data['first_participant'].id, value=10),
        data['first_user'], session,
    )

    with pytest.raises(HTTPException, match='cannot be removed'):
        await update_player_pool(
            data['championship'].id, UpdatePoolModel(player_ids=[data['auction'].player_id]), data['first_user'], session,
        )


async def test_cancelled_auction_player_can_leave_pool(session, auction_setup):
    data = auction_setup
    await cancel_auction(session, data['championship'].id, data['auction'].id)

    response = await update_player_pool(data['championship'].id, UpdatePoolModel(player_ids=[]), data['first_user'], session)

    assert response.player_ids == []
    assert await list_players(data['championship'].id, None, None, data['first_user'], session) == []


async def test_pool_cannot_change_after_draft(session, auction_setup):
    data = auction_setup
    data['championship'].status = 'games'
    await session.commit()

    with pytest.raises(HTTPException, match='only be changed during the draft'):
        await update_player_pool(
            data['championship'].id, UpdatePoolModel(player_ids=[data['auction'].player_id]), data['first_user'], session,
        )


async def test_player_outside_pool_cannot_be_assigned_or_auctioned(session, auction_setup):
    data = auction_setup
    [player] = await _add_players(session, data['auction'].player_id, [90])

    with pytest.raises(HTTPException, match='not part of this draft'):
        await buy_player(
            data['championship'].id, player.id,
            BuyPlayerModel(participant_id=data['first_participant'].id, value=10),
            data['first_user'], session,
        )
    with pytest.raises(HTTPException, match='not part of this draft'):
        await configure_auctions(session, data['championship'].id, [player.id], utc_now() + timedelta(hours=1), 10)


async def test_participant_team_lists_drafted_players_outside_pool(session, auction_setup):
    data = auction_setup
    [player] = await _add_players(session, data['auction'].player_id, [90])
    session.add(DraftPick(
        championship_id=data['championship'].id,
        participant_id=data['first_participant'].id,
        player_id=player.id,
        value=10,
    ))
    await session.commit()

    team = await list_players(data['championship'].id, None, data['first_participant'].id, data['first_user'], session)

    assert [p.id for p in team] == [player.id]


async def test_pool_identifies_owner_of_locked_players(session, auction_setup):
    data = auction_setup
    [player] = await _add_players(session, data['auction'].player_id, [90])
    session.add(DraftPick(
        championship_id=data['championship'].id,
        participant_id=data['first_participant'].id,
        player_id=player.id,
        value=10,
    ))
    await session.commit()

    pool = {p.id: p for p in await get_player_pool(data['championship'].id, data['first_user'], session)}

    assert pool[player.id].locked
    assert pool[player.id].participant_id == data['first_participant'].id
    assert pool[data['auction'].player_id].locked
    assert pool[data['auction'].player_id].participant_id is None
