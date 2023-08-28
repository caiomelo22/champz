# app/main.py

from fastapi import FastAPI

from app.routers import group, match, participant, player, position, team

app = FastAPI()

app.include_router(player.router, prefix="/player", tags=["player"])
app.include_router(position.router, prefix="/position", tags=["position"])
app.include_router(team.router, prefix="/team", tags=["team"])
app.include_router(participant.router, prefix="/participant", tags=["participant"])
app.include_router(match.router, prefix="/match", tags=["match"])
app.include_router(group.router, prefix="/group", tags=["group"])
