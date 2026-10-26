import asyncio
import os
import uuid
from datetime import timedelta
from urllib.parse import quote_plus

import mysql.connector
import pytest
import pytest_asyncio
from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.base import Base
from app.models_orm import Bid, Championship, Nation, Participant, Player, PlayerAuction, Position, Team, User
from app.services.auction import place_bid, utc_now


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_MYSQL_TESTS") != "1",
    reason="Set RUN_MYSQL_TESTS=1 to run isolated MySQL concurrency tests.",
)


@pytest_asyncio.fixture
async def mysql_session_factory():
    database_name = f"champz_test_{uuid.uuid4().hex}"
    connection = mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE `{database_name}` CHARACTER SET utf8mb4")
    cursor.close()
    connection.close()

    database_url = (
        f"mysql+asyncmy://{quote_plus(os.environ['DB_USER'])}:"
        f"{quote_plus(os.environ['DB_PASSWORD'])}@{os.environ['DB_HOST']}/{database_name}"
    )
    engine = create_async_engine(database_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    try:
        async with engine.begin() as db_connection:
            await db_connection.run_sync(Base.metadata.create_all)
        yield session_factory
    finally:
        await engine.dispose()
        connection = mysql.connector.connect(
            host=os.environ["DB_HOST"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
        )
        cursor = connection.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS `{database_name}`")
        cursor.close()
        connection.close()


async def _seed_auctions(session_factory, auction_count=1):
    async with session_factory() as session:
        first_user = User(
            id=uuid.uuid4(),
            email="first@example.com",
            hashed_password="unused",
            is_active=True,
            is_superuser=False,
            is_verified=True,
        )
        second_user = User(
            id=uuid.uuid4(),
            email="second@example.com",
            hashed_password="unused",
            is_active=True,
            is_superuser=False,
            is_verified=True,
        )
        championship = Championship(name="Concurrency", owner_id=first_user.id, budget_default=100)
        team = Team(name="Concurrency FC", image_path="team.png")
        nation = Nation(name="Concurrency", image_path="nation.png")
        position = Position(name="Attackers", specific_positions="ST")
        session.add_all([first_user, second_user, championship, team, nation, position])
        await session.flush()

        participants = [
            Participant(
                name="First",
                budget=100,
                championship_id=championship.id,
                user_id=first_user.id,
            ),
            Participant(
                name="Second",
                budget=100,
                championship_id=championship.id,
                user_id=second_user.id,
            ),
        ]
        players = [
            Player(
                id=f"concurrent-player-{index}",
                position_id=position.id,
                team_origin=team.name,
                name=f"Concurrent Player {index}",
                nation=nation.name,
                specific_position="ST",
                overall=80,
                pace=80,
                shooting=80,
                passing=80,
                dribbling=80,
                defending=40,
                physical=70,
                image_path="player.png",
            )
            for index in range(auction_count)
        ]
        session.add_all([*participants, *players])
        await session.flush()
        auctions = [
            PlayerAuction(
                championship_id=championship.id,
                player_id=player.id,
                deadline=utc_now() + timedelta(hours=1),
                minimum_bid=10,
            )
            for player in players
        ]
        session.add_all(auctions)
        await session.commit()
        return championship.id, [auction.id for auction in auctions], first_user.id, second_user.id


async def _bid(session_factory, championship_id, auction_id, user_id, amount):
    async with session_factory() as session:
        return await place_bid(session, championship_id, auction_id, user_id, amount)


async def test_concurrent_bids_on_same_player_keep_highest_bid(mysql_session_factory):
    championship_id, auction_ids, first_user_id, second_user_id = await _seed_auctions(
        mysql_session_factory
    )

    results = await asyncio.gather(
        _bid(mysql_session_factory, championship_id, auction_ids[0], first_user_id, 20),
        _bid(mysql_session_factory, championship_id, auction_ids[0], second_user_id, 30),
        return_exceptions=True,
    )

    assert not all(isinstance(result, Exception) for result in results)
    assert all(not isinstance(result, Exception) or isinstance(result, HTTPException) for result in results)
    async with mysql_session_factory() as session:
        auction = await session.get(PlayerAuction, auction_ids[0])
        participants = (await session.execute(select(Participant).order_by(Participant.id))).scalars().all()
        assert auction.leading_bid == 30
        assert sorted(participant.budget for participant in participants) == [70, 100]


async def test_concurrent_bids_cannot_overspend_one_participant(mysql_session_factory):
    championship_id, auction_ids, first_user_id, _ = await _seed_auctions(
        mysql_session_factory,
        auction_count=2,
    )

    results = await asyncio.gather(
        *[
            _bid(mysql_session_factory, championship_id, auction_id, first_user_id, 70)
            for auction_id in auction_ids
        ],
        return_exceptions=True,
    )

    assert sum(not isinstance(result, Exception) for result in results) == 1
    assert sum(isinstance(result, HTTPException) for result in results) == 1
    async with mysql_session_factory() as session:
        participant = (
            await session.execute(select(Participant).where(Participant.user_id == first_user_id))
        ).scalar_one()
        bid_count = (await session.execute(select(func.count(Bid.id)))).scalar_one()
        assert participant.budget == 30
        assert bid_count == 1