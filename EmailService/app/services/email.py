import asyncio
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from fastapi import BackgroundTasks, HTTPException, status
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db.models import Campaign, EmailLog, Subscriber
from app.core.email_templates import EmailTemplate

settings = get_settings()
logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.client = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        self.from_email = settings.SENDGRID_FROM_EMAIL
    
    async def send_email(
        self,
        to_emails: List[str],
        subject: str,
        content: str,
        is_html: bool = True,
        campaign_id: Optional[int] = None,
        db: Optional[Session] = None,
    ) -> List[Dict[str, Any]]:

        template = EmailTemplate.create_campaign_email(
            subject=subject,
            content=content,
            from_email=self.from_email,
            is_html=is_html
        )
        
        results = []
        
        batch_size = 1000
        for i in range(0, len(to_emails), batch_size):
            batch = to_emails[i:i+batch_size]
            batch_template = EmailTemplate.add_recipients(template.copy(), batch)
            
            try:
                response = self.client.send(batch_template)
                logger.info(f"Sent email batch {i//batch_size + 1}/{(len(to_emails)-1)//batch_size + 1}")
                
                if db and campaign_id:
                    for email in batch:
                        log = EmailLog(
                            recipient_email=email,
                            status="sent",
                            campaign_id=campaign_id,
                            message_id=response.headers.get("X-Message-Id")
                        )
                        db.add(log)
                    db.commit()
                
                results.append({
                    "status_code": response.status_code,
                    "batch_size": len(batch),
                    "message_id": response.headers.get("X-Message-Id")
                })
                
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Failed to send email batch: {str(e)}")
                if db and campaign_id:
                    for email in batch:
                        log = EmailLog(
                            recipient_email=email,
                            status="failed",
                            campaign_id=campaign_id,
                        )
                        db.add(log)
                    db.commit()
                
                results.append({
                    "status_code": 500,
                    "batch_size": len(batch),
                    "error": str(e)
                })
        
        return results
    
    def send_test_email(
        self,
        background_tasks: BackgroundTasks,
        campaign_id: int,
        test_emails: List[str],
        db: Session,
    ):
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if not campaign:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Campaign with ID {campaign_id} not found"
            )
        
        background_tasks.add_task(
            self.send_email,
            to_emails=test_emails,
            subject=f"[TEST] {campaign.subject}",
            content=campaign.body,
            is_html=campaign.is_html,
        )
        
        return {"message": f"Test email scheduled to be sent to {len(test_emails)} recipients"}
