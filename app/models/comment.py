from  sqlmodel import Field,Relationship,SQLModel
import random
import string
from uuid import uuid4,UUID
from .linked_tables import *
from typing import List
from datetime import datetime
from sqlalchemy import Column,DateTime
from sqlalchemy.sql import func


class Comment(SQLModel,table=True):
    id: UUID  = Field(default_factory=uuid4,primary_key=True,index=True)
    content:str
    user_id:UUID = Field(foreign_key="user.id")
    post_id:UUID = Field(foreign_key="post.id")
    user:"User" = Relationship(back_populates='user_comments')
    post:"Post" = Relationship(back_populates='post_comments')
    visible:bool = Field(default=True)
    created_at: datetime = Field(sa_column=Column(DateTime,default=func.now(),nullable=True))
    updated_at: datetime = Field(sa_column=Column(DateTime,default=func.now(),nullable=True,onupdate=func.now()))
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
    comment_liked_users:List["UserResponse"]
