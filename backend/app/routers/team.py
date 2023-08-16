import typing as t

from fastapi import APIRouter, HTTPException

from app.db.league import check_league_exists
from app.db.team import get_teams_by_league
from app.models.team import team

router = APIRouter()


@router.get("/list/league/{league_id}")
def list_by_league(league_id: int) -> t.List[team]:
    league_exists = check_league_exists(league_id)
    if not league_exists:
        raise HTTPException(status_code=404, detail="League not found.")

    teams = get_teams_by_league(league_id)
    return teams
