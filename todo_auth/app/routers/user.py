from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.schemas import UserCreate, UserResponse
from app.database.models import User
from app.database.database import get_db
from app.core.security import hash_password

router = APIRouter()

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
