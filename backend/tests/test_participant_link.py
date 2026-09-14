import uuid

from app.models_orm import Championship, Participant, User
from app.services.participant_link import (
    normalize_email,
    resolve_pending_participant_links_in_session,
)


def test_normalize_email_strips_and_casefolds():
    assert normalize_email("  Person@Example.COM ") == "person@example.com"


async def test_resolves_one_pending_link_per_championship(session):
    user = User(
        id=uuid.uuid4(),
        email="person@example.com",
        hashed_password="unused",
        is_active=True,
        is_superuser=False,
        is_verified=True,
    )
    first_championship = Championship(name="First", owner_id=user.id, budget_default=100)
    second_championship = Championship(name="Second", owner_id=user.id, budget_default=100)
    session.add_all([user, first_championship, second_championship])
    await session.flush()

    linked = Participant(
        name="Already linked",
        budget=100,
        championship_id=first_championship.id,
        user_id=user.id,
    )
    conflicting = Participant(
        name="Conflicting invitation",
        budget=100,
        championship_id=first_championship.id,
        pending_user_email=user.email,
    )
    pending = Participant(
        name="Pending",
        budget=100,
        championship_id=second_championship.id,
        pending_user_email=user.email,
    )
    session.add_all([linked, conflicting, pending])
    await session.flush()

    linked_count = await resolve_pending_participant_links_in_session(
        session,
        user.id,
        " Person@Example.COM ",
    )
    await session.flush()

    assert linked_count == 1
    assert pending.user_id == user.id
    assert pending.pending_user_email is None
    assert conflicting.user_id is None
    assert conflicting.pending_user_email == user.email