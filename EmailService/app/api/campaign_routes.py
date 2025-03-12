from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.api.dependencies import get_current_active_user
from app.db.session import get_db
from app.db.models import Campaign, SubscriberList
from app.schemas import email as email_schemas
from app.services.email import EmailService
from app.services.campaign import CampaignService

router = APIRouter()

email_service = EmailService()
campaign_service = CampaignService(email_service)

@router.post("/campaigns", response_model=email_schemas.Campaign)
def create_campaign(
    campaign_in: email_schemas.CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Campaign:
    subscriber_list = db.query(SubscriberList).filter(SubscriberList.id == campaign_in.list_id).first()
    if not subscriber_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"List with ID {campaign_in.list_id} not found",
        )
    
    campaign = Campaign(
        name=campaign_in.name,
        subject=campaign_in.subject,
        body=campaign_in.body,
        is_html=campaign_in.is_html,
        scheduled_at=campaign_in.scheduled_at,
        owner_id=current_user.id,
        list_id=campaign_in.list_id,
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    
    return campaign

@router.get("/campaigns", response_model=List[email_schemas.Campaign])
def get_campaigns(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[Campaign]:
    campaigns = db.query(Campaign).filter(
        Campaign.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    return campaigns

@router.get("/campaigns/{campaign_id}", response_model=email_schemas.Campaign)
def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Campaign:
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.owner_id == current_user.id
    ).first()
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with ID {campaign_id} not found",
        )
    return campaign
