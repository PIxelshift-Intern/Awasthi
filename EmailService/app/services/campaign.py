from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.db.models import Campaign, EmailLog, Subscriber, SubscriberList
from app.services.email import EmailService

logger = logging.getLogger(__name__)


class CampaignService:
    def __init__(self, email_service: EmailService):
        self.email_service = email_service
    
    async def send_campaign(
        self,
        background_tasks: BackgroundTasks,
        campaign_id: int,
        send_now: bool = True,
        db: Session = None,
    ) -> Dict[str, Any]:

        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if not campaign:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Campaign with ID {campaign_id} not found"
            )
        
        if campaign.sent_at is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Campaign with ID {campaign_id} was already sent at {campaign.sent_at}"
            )
        
        subscribers = db.query(Subscriber).join(
            SubscriberList.subscribers
        ).filter(
            SubscriberList.id == campaign.list_id,
            Subscriber.is_active == True
        ).all()
        
        if not subscribers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No active subscribers found in the list for campaign {campaign_id}"
            )
        
        subscriber_emails = [subscriber.email for subscriber in subscribers]
        
        if send_now:
            campaign.sent_at = datetime.utcnow()
            db.commit()
            
            background_tasks.add_task(
                self.email_service.send_email,
                to_emails=subscriber_emails,
                subject=campaign.subject,
                content=campaign.body,
                is_html=campaign.is_html,
                campaign_id=campaign.id,
                db=db,
            )
            
            return {
                "message": f"Campaign scheduled to be sent to {len(subscriber_emails)} recipients",
                "campaign_id": campaign.id,
                "recipient_count": len(subscriber_emails)
            }
        else:
            return {
                "message": f"Campaign is scheduled for {campaign.scheduled_at}",
                "campaign_id": campaign.id,
                "recipient_count": len(subscriber_emails),
                "scheduled_at": campaign.scheduled_at
            }
    
    def get_campaign_stats(self, campaign_id: int, db: Session) -> Dict[str, Any]:

        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if not campaign:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Campaign with ID {campaign_id} not found"
            )
        
        stats = db.query(
            func.count(EmailLog.id).label("total"),
            func.sum(func.case((EmailLog.status == "sent", 1), else_=0)).label("sent"),
            func.sum(func.case((EmailLog.status == "delivered", 1), else_=0)).label("delivered"),
            func.sum(func.case((EmailLog.status == "opened", 1), else_=0)).label("opened"),
            func.sum(func.case((EmailLog.status == "clicked", 1), else_=0)).label("clicked"),
            func.sum(func.case((EmailLog.status == "bounced", 1), else_=0)).label("bounced"),
        ).filter(EmailLog.campaign_id == campaign_id).first()
        
        return {
            "campaign_id": campaign.id,
            "name": campaign.name,
            "subject": campaign.subject,
            "created_at": campaign.created_at,
            "sent_at": campaign.sent_at,
            "total": stats.total or 0,
            "sent": stats.sent or 0,
            "delivered": stats.delivered or 0,
            "opened": stats.opened or 0,
            "clicked": stats.clicked or 0,
            "bounced": stats.bounced or 0,
            "open_rate": (stats.opened / stats.delivered * 100) if stats.delivered else 0,
            "click_rate": (stats.clicked / stats.opened * 100) if stats.opened else 0,
            "bounce_rate": (stats.bounced / stats.sent * 100) if stats.sent else 0,
        }