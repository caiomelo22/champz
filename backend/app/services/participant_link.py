import uuid

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import async_session_maker
from app.models_orm.participant import Participant


def normalize_email(email: str) -> str:
    return email.strip().casefold()


async def resolve_pending_participant_links(user_id: uuid.UUID, email: str) -> int:
    async with async_session_maker() as session:
        linked_count = await resolve_pending_participant_links_in_session(
            session,
            user_id,
            email,
        )
        await session.commit()
        return linked_count


async def resolve_pending_participant_links_in_session(
    session: AsyncSession,
    user_id: uuid.UUID,
    email: str,
) -> int:
    normalized_email = normalize_email(email)
    rows = (
        await session.execute(
            select(Participant)
            .where(
                or_(
                    Participant.pending_user_email == normalized_email,
                    Participant.user_id == user_id,
                )
            )
            .order_by(Participant.id)
            .with_for_update()
        )
    ).scalars().all()

    linked_championship_ids = {
        participant.championship_id
        for participant in rows
        if participant.user_id == user_id
    }
    linked_count = 0

    for participant in rows:
        if participant.pending_user_email != normalized_email:
            continue
        if participant.championship_id in linked_championship_ids:
            continue

        participant.user_id = user_id
        participant.pending_user_email = None
        linked_championship_ids.add(participant.championship_id)
        linked_count += 1

    return linked_count