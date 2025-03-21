from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from database.models import Comment, BlogPost
from schemas.comment import CommentCreate, Comment
from typing import List
from routers.blog import get_current_user
from database.models import User

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/{post_id}", response_model=Comment)
async def create_comment(post_id: int, comment: CommentCreate, user: User = Depends(get_current_user), 
                       db: Session = Depends(get_db)):
    blog = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    db_comment = Comment(**comment.dict(), user_id=user.id, post_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.post("/{post_id}/{parent_comment_id}", response_model=Comment)
async def create_reply(post_id: int, parent_comment_id: int, comment: CommentCreate, 
                      user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    blog = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    parent = db.query(Comment).filter(Comment.id == parent_comment_id).first()
    if not blog or not parent:
        raise HTTPException(status_code=404, detail="Blog or parent comment not found")
    db_comment = Comment(**comment.dict(), user_id=user.id, post_id=post_id, 
                        parent_comment_id=parent_comment_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/{post_id}", response_model=List[Comment])
async def read_comments(post_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.post_id == post_id, Comment.parent_comment_id == None).all()