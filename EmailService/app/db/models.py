from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.db.session import Base


class Subscriber(Base):
    __tablename__ = "subscribers"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    lists = relationship(
        "SubscriberList",
        secondary="list_subscribers",
        back_populates="subscribers"
    )


list_subscribers = Table(
    "list_subscribers",
    Base.metadata,
    Column("list_id", Integer, ForeignKey("subscriber_lists.id"), primary_key=True),
    Column("subscriber_id", Integer, ForeignKey("subscribers.id"), primary_key=True),
)


class SubscriberList(Base):
    __tablename__ = "subscriber_lists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    subscribers = relationship(
        "Subscriber",
        secondary="list_subscribers",
        back_populates="lists"
    )
    campaigns = relationship("Campaign", back_populates="subscriber_list")


class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject = Column(String)
    body = Column(Text)
    is_html = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    scheduled_at = Column(DateTime, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    list_id = Column(Integer, ForeignKey("subscriber_lists.id"))
    
    owner = relationship("User", back_populates="campaigns")
    subscriber_list = relationship("SubscriberList", back_populates="campaigns")
    email_logs = relationship("EmailLog", back_populates="campaign")


class EmailLog(Base):
    __tablename__ = "email_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    recipient_email = Column(String, index=True)
    status = Column(String)  # sent, delivered, opened, clicked, bounced, etc.
    sent_at = Column(DateTime, default=datetime.utcnow)
    message_id = Column(String, nullable=True)  # SendGrid message ID
    
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    
    campaign = relationship("Campaign", back_populates="email_logs")