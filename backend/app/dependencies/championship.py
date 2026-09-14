from dataclasses import dataclass
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models_orm.championship import Championship
from app.models_orm.participant import Participant
from app.models_orm.user import User


@dataclass
class ChampionshipAccess:
    championship: Championship
    role: str
    participant: Optional[Participant]


async def get_championship_access(
    session: AsyncSession,
    championship_id: int,
    user: User,
) -> ChampionshipAccess:
    championship = (
        await session.execute(
            select(Championship).where(Championship.id == championship_id)
        )
    ).scalar_one_or_none()
    if not championship:
        raise HTTPException(status_code=404, detail="Championship not found.")

    participant = None
    if user.is_verified:
        participant = (
            await session.execute(
                select(Participant).where(
                    Participant.championship_id == championship_id,
                    Participant.user_id == user.id,
                )
            )
        ).scalar_one_or_none()

    if championship.owner_id == user.id:
        return ChampionshipAccess(championship, "owner", participant)
    if participant:
        return ChampionshipAccess(championship, "participant", participant)

    raise HTTPException(status_code=404, detail="Championship not found.")


def require_owner(access: ChampionshipAccess) -> None:
    if access.role != "owner":
        raise HTTPException(status_code=403, detail="Championship owner access required.")