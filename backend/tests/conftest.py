import uuid
from datetime import timedelta

import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models_orm import Championship, ChampionshipPlayer, Nation, Participant, Player, PlayerAuction, Position, Team, User
from app.services.auction import utc_now


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as test_session:
        yield test_session

    await engine.dispose()


@pytest_asyncio.fixture
async def auction_setup(session):
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
    championship = Championship(name="Test", owner_id=first_user.id, budget_default=100)
    team = Team(name="Test FC", image_path="team.png")
    nation = Nation(name="Testland", image_path="nation.png")
    position = Position(name="Attackers", specific_positions="ST")
    session.add_all([first_user, second_user, championship, team, nation, position])
    await session.flush()

    player = Player(
        id="test-player",
        position_id=position.id,
        team_origin=team.name,
        name="Test Player",
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
    first_participant = Participant(
        name="First",
        budget=100,
        championship_id=championship.id,
        user_id=first_user.id,
    )
    second_participant = Participant(
        name="Second",
        budget=100,
        championship_id=championship.id,
        user_id=second_user.id,
    )
    session.add_all([player, first_participant, second_participant])
    await session.flush()

    auction = PlayerAuction(
        championship_id=championship.id,
        player_id=player.id,
        deadline=utc_now() + timedelta(hours=1),
        minimum_bid=10,
    )
    session.add_all([auction, ChampionshipPlayer(championship_id=championship.id, player_id=player.id)])
    await session.commit()

    return {
        "championship": championship,
        "auction": auction,
        "first_user": first_user,
        "second_user": second_user,
        "first_participant": first_participant,
        "second_participant": second_participant,
    }