import typing as t

from fastapi import APIRouter

from app.db.team import get_most_popular_teams
from app.models.team import team

router = APIRouter()


@router.get("/most-popular")
def most_popular() -> t.List[team]:
    return get_most_popular_teams()
