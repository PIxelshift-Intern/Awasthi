from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    user_id: int
    post_id: int
    parent_comment_id: Optional[int]
    created_at: datetime
    class Config:
        orm_mode = True