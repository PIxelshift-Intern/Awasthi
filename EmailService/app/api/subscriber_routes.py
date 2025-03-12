from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.api.dependencies import get_current_active_user
from app.db.session import get_db
from app.db.models import Subscriber, SubscriberList
from app.schemas import email as email_schemas

router = APIRouter()

@router.post("/subscribers", response_model=email_schemas.Subscriber)
def create_subscriber(
    subscriber_in: email_schemas.SubscriberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Subscriber:
    subscriber = db.query(Subscriber).filter(Subscriber.email == subscriber_in.email).first()
    if subscriber:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already subscribed",
        )
    
    subscriber = Subscriber(
        email=subscriber_in.email,
        name=subscriber_in.name,
    )
    db.add(subscriber)
    db.commit()
    db.refresh(subscriber)
    
    return subscriber

@router.get("/subscribers", response_model=List[email_schemas.Subscriber])
def get_subscribers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[Subscriber]:
    subscribers = db.query(Subscriber).offset(skip).limit(limit).all()
    return subscribers

@router.get("/subscribers/{subscriber_id}", response_model=email_schemas.Subscriber)
def get_subscriber(
    subscriber_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Subscriber:
    subscriber = db.query(Subscriber).filter(Subscriber.id == subscriber_id).first()
    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscriber with ID {subscriber_id} not found",
        )
    return subscriber

@router.get("/subscribers/list/{list_id}", response_model=List[email_schemas.Subscriber])
def get_subscribers_by_list(
    list_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[Subscriber]:
    subscribers = db.query(Subscriber).filter(Subscriber.list_id == list_id).all()
    if not subscribers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No subscribers found for list ID {list_id}",
        )
    return subscribers
