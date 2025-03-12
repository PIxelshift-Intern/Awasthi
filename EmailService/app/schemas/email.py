from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class SubscriberBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class SubscriberCreate(SubscriberBase):
    pass


class SubscriberUpdate(SubscriberBase):
    is_active: Optional[bool] = None


class Subscriber(SubscriberBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class SubscriberListBase(BaseModel):
    name: str
    description: Optional[str] = None


class SubscriberListCreate(SubscriberListBase):
    pass


class SubscriberListUpdate(SubscriberListBase):
    pass


class SubscriberList(SubscriberListBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class SubscriberListWithMembers(SubscriberList):
    subscribers: List[Subscriber] = []


class CampaignBase(BaseModel):
    name: str
    subject: str
    body: str
    is_html: bool = True
    scheduled_at: Optional[datetime] = None


class CampaignCreate(CampaignBase):
    list_id: int


class CampaignUpdate(CampaignBase):
    list_id: Optional[int] = None


class Campaign(CampaignBase):
    id: int
    created_at: datetime
    sent_at: Optional[datetime] = None
    owner_id: int
    list_id: int
    
    class Config:
        from_attributes = True


class EmailLogBase(BaseModel):
    recipient_email: EmailStr
    status: str
    message_id: Optional[str] = None


class EmailLog(EmailLogBase):
    id: int
    sent_at: datetime
    campaign_id: int
    
    class Config:
        from_attributes = True


class CampaignWithStats(Campaign):
    total_sent: int = 0
    delivered: int = 0
    opened: int = 0
    clicked: int = 0
    bounced: int = 0


class SendTestEmail(BaseModel):
    campaign_id: int
    test_emails: List[EmailStr]


class SendCampaign(BaseModel):
    campaign_id: int
    send_now: bool = True