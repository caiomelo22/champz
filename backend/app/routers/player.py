# routes/users.py
from fastapi import APIRouter
from app.db.players import get_players

router = APIRouter()

@router.get("/list")
def read_users():
    return get_players()
