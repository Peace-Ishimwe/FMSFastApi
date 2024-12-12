from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from .database import get_db
from .models import Campaign as CampaignModel, User as UserModel
from .schemas import CampaignCreate, CampaignUpdate, CampaignResponse
from .dependencies import get_current_user

app = FastAPI()

@app.get("/campaigns", response_model=List[CampaignResponse])
def list_campaigns(db: Session = Depends(get_db)):
    campaigns = db.query(CampaignModel).all()
    return campaigns

@app.post("/campaigns", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
def create_campaign(campaign: CampaignCreate, 
                    db: Session = Depends(get_db),
                    current_user: UserModel = Depends(get_current_user)):
    if current_user.role != 'Admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create a campaign."
        )
    new_campaign = CampaignModel(**campaign.dict(), created_by_id=current_user.id)
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return new_campaign

@app.get("/campaigns/{campaign_id}", response_model=CampaignResponse)
def get_campaign_detail(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(CampaignModel).filter(CampaignModel.id == campaign_id).first()
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found."
        )
    return campaign

@app.put("/campaigns/{campaign_id}", response_model=CampaignResponse)
def update_campaign(campaign_id: int, 
                    campaign_data: CampaignUpdate, 
                    db: Session = Depends(get_db),
                    current_user: UserModel = Depends(get_current_user)):
    campaign = db.query(CampaignModel).filter(CampaignModel.id == campaign_id).first()
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found."
        )

    if current_user.id != campaign.created_by_id and current_user.role != 'Admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this campaign."
        )

    for key, value in campaign_data.dict(exclude_unset=True).items():
        setattr(campaign, key, value)

    db.commit()
    db.refresh(campaign)
    return campaign
