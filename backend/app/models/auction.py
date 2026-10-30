import typing as t
from datetime import datetime

from pydantic import BaseModel, Field


class ConfigureAuctionsModel(BaseModel):
    player_ids: list[str] = Field(min_length=1)
    deadline: datetime
    minimum_bid: int = Field(gt=0)


class UpdateAuctionModel(BaseModel):
    deadline: datetime
    minimum_bid: int = Field(gt=0)


class PlaceBidModel(BaseModel):
    amount: int = Field(gt=0)
    participant_id: t.Optional[int] = None


class AuctionResponse(BaseModel):
    id: int
    player_id: str
    player_name: str
    deadline: datetime
    minimum_bid: int
    status: str
    leading_participant_id: t.Optional[int] = None
    leading_participant_name: t.Optional[str] = None
    leading_bid: t.Optional[int] = None
    bid_count: int = 0
    is_current_user_leader: bool = False


class BidResultResponse(BaseModel):
    auction: AuctionResponse
    available_budget: int
