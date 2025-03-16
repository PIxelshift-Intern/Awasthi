from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.db import Base

list_subscribers = Table(
    "list_subscribers",
    Base.metadata,
    Column("list_id", Integer, ForeignKey("subscriber_lists.id"), primary_key=True),
    Column("subscriber_id", Integer, ForeignKey("subscribers.id"), primary_key=True),
)

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

class SubscriberList(Base):
    __tablename__ = "subscriber_lists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    subscribers = relationship(
        "Subscriber",
        secondary="list_subscribers",
        back_populates="lists"
    )

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject = Column(String)
    body = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)
    list_id = Column(Integer, ForeignKey("subscriber_lists.id"))
    subscriber_list = relationship("SubscriberList")