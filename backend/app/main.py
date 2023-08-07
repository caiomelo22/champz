# app/main.py

from fastapi import FastAPI
from app.routers import player

app = FastAPI()

app.include_router(player.router, prefix="/players", tags=["users"])
