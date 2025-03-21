from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from database.models import BlogPost, User
from schemas.blog import BlogCreate, Blog
from typing import List
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

router = APIRouter(prefix="/blogs", tags=["blogs"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid authentication")
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid authentication")

@router.post("/", response_model=Blog)
async def create_blog(blog: BlogCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_blog = BlogPost(**blog.dict(), user_id=user.id)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

@router.get("/", response_model=List[Blog])
async def read_blogs(db: Session = Depends(get_db)):
    return db.query(BlogPost).all()

@router.get("/{blog_id}", response_model=Blog)
async def read_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.put("/{blog_id}", response_model=Blog)
async def update_blog(blog_id: int, blog: BlogCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_blog = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
    if db_blog is None or db_blog.user_id != user.id:
        raise HTTPException(status_code=404, detail="Blog not found or unauthorized")
    for key, value in blog.dict().items():
        setattr(db_blog, key, value)
    db.commit()
    db.refresh(db_blog)
    return db_blog

@router.delete("/{blog_id}")
async def delete_blog(blog_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_blog = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
    if db_blog is None or db_blog.user_id != user.id:
        raise HTTPException(status_code=404, detail="Blog not found or unauthorized")
    db.delete(db_blog)
    db.commit()
    return {"message": "Blog deleted"}