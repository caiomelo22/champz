from typing import List

from fastapi import APIRouter

from app.db.league import get_leagues
from app.models.league import league

router = APIRouter()


@router.get("/list")
def list_leagues() -> List[league]:
    return get_leagues()
