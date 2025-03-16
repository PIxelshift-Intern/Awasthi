from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class SubscriberBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class SubscriberCreate(SubscriberBase):
    list_id: int

class SubscriberResponse(SubscriberBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True 

class CampaignBase(BaseModel):
    name: str
    subject: str
    body: str

class CampaignCreate(CampaignBase):
    list_id: int

class CampaignResponse(CampaignBase):
    id: int
    created_at: datetime
    sent_at: Optional[datetime] = None
    list_id: int
    
    class Config:
        from_attributes = True
        model_config = {"populate_by_name": True}
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Welcome Campaign",
                "subject": "Welcome to our service",
                "body": "Thank you for subscribing!",
                "created_at": "2023-01-01T00:00:00",
                "sent_at": None,
                "list_id": 1
            }
        }
        field_customization = {
            "body": {"alias": "body"}
        }

class MessageResponse(BaseModel):
    message: str
    campaign_id: Optional[int] = None
    subscriber_count: Optional[int] = None

class ListResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True