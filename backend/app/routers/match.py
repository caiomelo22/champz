import typing as t

from fastapi import APIRouter, HTTPException

from app.db.match import (
    check_match_exists,
    create_matches,
    update_match,
)
from app.models.match import create_match_model, match, update_match_model

router = APIRouter()


@router.patch("/update")
def create(data: update_match_model) -> None:
    match_exists = check_match_exists(data.match_id)
    if not match_exists:
        raise HTTPException(status_code=404, detail="Match not found.")

    update_match(data)
