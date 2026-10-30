from typing import Iterable

from fastapi import HTTPException
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models_orm.championship import Championship
from app.models_orm.championship_player import ChampionshipPlayer
from app.models_orm.draft_pick import DraftPick
from app.models_orm.player import Player
from app.models_orm.player_auction import PlayerAuction
from app.models_orm.position import Position

# Players per participant suggested for each position when creating a championship.
LIMIT_BY_POSITION = {
    "Goalkeepers": 1,
    "Center Backs": 3,
    "Full Backs": 2.5,
    "Defensive Midfielders": 3,
    "Ofensive Midfielders": 1.5,
    "Wingers": 2.5,
    "Attackers": 2,
}


def pool_player_ids_stmt(championship_id: int):
    return select(ChampionshipPlayer.player_id).where(ChampionshipPlayer.championship_id == championship_id)


async def get_pool_player_ids(session: AsyncSession, championship_id: int) -> set[str]:
    return set((await session.execute(pool_player_ids_stmt(championship_id))).scalars().all())


async def suggest_player_ids(session: AsyncSession, num_participants: int) -> set[str]:
    """Top players of each position according to LIMIT_BY_POSITION and the number of participants."""
    suggested = set()
    positions = (await session.execute(select(Position))).scalars().all()
    for position in positions:
        factor = LIMIT_BY_POSITION.get(position.name)
        limit = int(num_participants * factor) if factor else 0
        if limit <= 0:
            continue
        ids = (
            await session.execute(
                select(Player.id)
                .where(Player.position_id == position.id)
                .order_by(Player.overall.desc(), Player.pace.desc())
                .limit(limit)
            )
        ).scalars().all()
        suggested.update(ids)
    return suggested


async def get_locked_player_ids(session: AsyncSession, championship_id: int) -> set[str]:
    """Players that cannot leave the pool: assigned to a participant or with an open auction."""
    drafted = (
        await session.execute(select(DraftPick.player_id).where(DraftPick.championship_id == championship_id))
    ).scalars().all()
    auctioned = (
        await session.execute(
            select(PlayerAuction.player_id).where(
                PlayerAuction.championship_id == championship_id,
                PlayerAuction.status == "open",
            )
        )
    ).scalars().all()
    return set(drafted) | set(auctioned)


async def _validate_player_ids(session: AsyncSession, player_ids: set[str]) -> None:
    if not player_ids:
        return
    existing = set(
        (await session.execute(select(Player.id).where(Player.id.in_(player_ids)))).scalars().all()
    )
    if existing != player_ids:
        raise HTTPException(status_code=404, detail="One or more players were not found.")


async def add_pool_players(session: AsyncSession, championship_id: int, player_ids: Iterable[str]) -> None:
    ids = set(player_ids)
    await _validate_player_ids(session, ids)
    if ids:
        await session.execute(
            insert(ChampionshipPlayer),
            [{"championship_id": championship_id, "player_id": player_id} for player_id in sorted(ids)],
        )


async def replace_pool(session: AsyncSession, championship_id: int, player_ids: Iterable[str]) -> set[str]:
    """Replace the championship pool. Locked players must remain selected. Caller commits."""
    requested = set(player_ids)

    championship = (
        await session.execute(
            select(Championship).where(Championship.id == championship_id).with_for_update()
        )
    ).scalar_one()
    if championship.status != "draft":
        raise HTTPException(status_code=409, detail="The draft pool can only be changed during the draft.")

    missing_locked = await get_locked_player_ids(session, championship_id) - requested
    if missing_locked:
        raise HTTPException(
            status_code=409,
            detail="Players assigned to a participant or with an open auction cannot be removed from the draft.",
        )

    current = await get_pool_player_ids(session, championship_id)
    removed = current - requested
    if removed:
        await session.execute(
            delete(ChampionshipPlayer).where(
                ChampionshipPlayer.championship_id == championship_id,
                ChampionshipPlayer.player_id.in_(removed),
            )
        )
    await add_pool_players(session, championship_id, requested - current)
    return requested


async def ensure_in_pool(session: AsyncSession, championship_id: int, player_ids: Iterable[str]) -> None:
    ids = set(player_ids)
    in_pool = (
        await session.execute(pool_player_ids_stmt(championship_id).where(ChampionshipPlayer.player_id.in_(ids)))
    ).scalars().all()
    if set(in_pool) != ids:
        raise HTTPException(status_code=409, detail="One or more players are not part of this draft.")
