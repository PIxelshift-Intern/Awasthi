from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.services.email import EmailService
from app.config import get_settings
from app.db.models import Subscriber, SubscriberList, Campaign
from app.schemas.email import (
    SubscriberCreate, SubscriberResponse,
    CampaignCreate, CampaignResponse,
    MessageResponse, ListResponse
)
from datetime import datetime

router = APIRouter()
settings = get_settings()
email_service = EmailService()

@router.post("/lists", response_model=ListResponse)
def create_list(list_name: str, db: Session = Depends(get_db)):
    db_list = SubscriberList(name=list_name)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

@router.post("/subscribers", response_model=SubscriberResponse)
def add_subscriber(
    subscriber: SubscriberCreate,
    db: Session = Depends(get_db)
):
    # Check if subscriber exists
    db_subscriber = db.query(Subscriber).filter(Subscriber.email == subscriber.email).first()
    if db_subscriber:
        raise HTTPException(status_code=400, detail="Email already subscribed")
    
    # Check if list exists
    db_list = db.query(SubscriberList).filter(SubscriberList.id == subscriber.list_id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="Subscriber list not found")
    
    # Create and add subscriber to list
    db_subscriber = Subscriber(email=subscriber.email, name=subscriber.name)
    db_list.subscribers.append(db_subscriber)
    db.add(db_subscriber)
    db.commit()
    db.refresh(db_subscriber)
    
    return db_subscriber

@router.post("/campaigns", response_model=CampaignResponse)
def create_campaign(
    campaign: CampaignCreate,
    db: Session = Depends(get_db)
):
    # Check if list exists
    db_list = db.query(SubscriberList).filter(SubscriberList.id == campaign.list_id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="Subscriber list not found")
    
    # Create campaign
    db_campaign = Campaign(
        name=campaign.name,
        subject=campaign.subject,
        body=campaign.body,
        list_id=campaign.list_id
    )
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    
    return db_campaign

@router.post("/campaigns/{campaign_id}/send", response_model=MessageResponse)
def send_campaign(
    campaign_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Get campaign
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Get subscribers
    subscribers = db.query(Subscriber).join(Subscriber.lists).filter(
        Subscriber.lists.any(id=campaign.list_id),
        Subscriber.is_active == True
    ).all()
    
    if not subscribers:
        raise HTTPException(status_code=400, detail="No active subscribers in list")
    
    emails = [sub.email for sub in subscribers]
    campaign.sent_at = datetime.utcnow()
    db.commit()
    
    # Schedule email sending
    background_tasks.add_task(
        email_service.send_email,
        to_emails=emails,
        subject=campaign.subject,
        content=campaign.body
    )
    
    return MessageResponse(
        message=f"Campaign scheduled to send to {len(emails)} subscribers",
        campaign_id=campaign_id,
        subscriber_count=len(emails)
    )