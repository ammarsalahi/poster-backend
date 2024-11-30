from core import BaseModel
from  sqlmodel import Field,Relationship,SQLModel
import random
import string
from uuid import uuid4,UUID
from .linked_tables import *
from typing import List
from datetime import datetime
from .user import UserResponse

class Comment(BaseModel,SQLModel,table=True):
    content:str
    user_id:UUID | None = Field(default=None,foreign_key="user.id")
    post_id:UUID|None = Field(default=None,foreign_key="post.id")
    user:"User" = Relationship(back_populates='user_comments')
    post:"Post" = Relationship(back_populates='post_comments')
    visible:bool = Field(default=True)
    comment_liked_users:List["User"] = Relationship(back_populates='liked_comments')


class CommentAdd(SQLModel):
    content:str 
    post_id:UUID
    user_id:UUID

class CommentEdit(SQLModel):
    content:str|None=None  

class CommentResponse(SQLModel):
    id:UUID
    content:str 
    user_id:UUID
    post_id:UUID
    created_at:datetime
    updated_at:datetime
    visible:bool
    comment_liked_users:List[UserResponse]
    





