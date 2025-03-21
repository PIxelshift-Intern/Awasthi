from pydantic import BaseModel
from datetime import datetime

class BlogBase(BaseModel):
    title: str
    content: str

class BlogCreate(BlogBase):
    pass

class Blog(BlogBase):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        orm_mode = True