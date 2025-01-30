from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..schemas import BlogPostCreate, BlogPostResponse
from ..core.security import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=BlogPostResponse)
def create_post(post: BlogPostCreate, db: Session = Depends(SessionLocal), user=Depends(get_current_user)):
    db_post = BlogPost(**post.dict(), author_id=user.id)
    db.add(db_post)
    db.commit()
    return db_post

@router.get("/{post_id}", response_model=BlogPostResponse)
def read_post(post_id: int, db: Session = Depends(SessionLocal)):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post