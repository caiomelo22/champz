# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import (group, match, participant, player, position,
                         team)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure CORS settings
origins = [
    "http://localhost:8080",  # Add your frontend's origin here
    # Other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(player.router, prefix="/player", tags=["player"])
app.include_router(position.router, prefix="/position", tags=["position"])
app.include_router(team.router, prefix="/team", tags=["team"])
app.include_router(participant.router, prefix="/participant", tags=["participant"])
app.include_router(match.router, prefix="/match", tags=["match"])
app.include_router(group.router, prefix="/group", tags=["group"])
