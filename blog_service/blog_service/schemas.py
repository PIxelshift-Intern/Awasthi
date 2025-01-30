from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class BlogPostCreate(BaseModel):
    title: str
    content: str

class BlogPostResponse(BlogPostCreate):
    id: int
    author_id: int
    created_at: datetime