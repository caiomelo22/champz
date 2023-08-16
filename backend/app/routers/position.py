import typing as t

from fastapi import APIRouter

from app.db.position import list_positions
from app.models.position import position

router = APIRouter()


@router.get("/list")
def list() -> t.List[position]:
    return list_positions()
