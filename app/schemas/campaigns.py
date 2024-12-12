from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# Pydantic Schemas

class FundingBase(BaseModel):
    amount: float
    funded_at: Optional[datetime] = None


class FundingCreate(FundingBase):
    campaign_id: int
    user_id: int


class FundingResponse(FundingBase):
    id: int
    user_id: int
    campaign_id: int

    class Config:
        orm_mode = True


class CampaignBase(BaseModel):
    name: str
    description: Optional[str] = None
    goal_amount: float


class CampaignCreate(CampaignBase):
    created_by_id: int


class CampaignResponse(CampaignBase):
    id: int
    created_by_id: int
    created_at: datetime
    updated_at: datetime
    total_funded: Optional[float] = 0.0
    fundings: List[FundingResponse] = []

    class Config:
        orm_mode = True
