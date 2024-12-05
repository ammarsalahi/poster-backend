from sqlmodel import Field,Relationship,SQLModel
import random
import string
from uuid import uuid4,UUID
from .linked_tables import *
from typing import List
from utils.uid_tool import get_uid
from datetime import datetime
from sqlalchemy import Column,DateTime
from sqlalchemy.sql import func

class Post(SQLModel,table=True):

    id: UUID  = Field(default_factory=uuid4,primary_key=True,index=True)
    post_id:str=Field(unique=True,index=True,default=lambda:get_uid())
    content:str | None = None
    views:int = Field(default=0)
    post_type:str = Field(default="public")
    visible:bool = Field(default=True)
    user_id:UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(sa_column=Column(DateTime,default=func.now(),nullable=True))
    updated_at: datetime = Field(sa_column=Column(DateTime,default=func.now(),nullable=True,onupdate=func.now()))
    user:"User" = Relationship(back_populates='user_posts')
    post_comments:List["Comment"] =Relationship(back_populates='post')
    medias:List["Media"] = Relationship(back_populates="post")
    post_liked_users:List["User"] = Relationship(back_populates='liked_posts',link_model=UserPostLink)


class PostAdd(SQLModel):
    content:str|None=None
    post_type:str|None=None
    medias:List[str]
    user_id:UUID

class PostEdit(SQLModel):
    content:str|None=None
    post_type:str|None=None
    medias:List[UUID]|None=None

class PostResponse(SQLModel):
    post_id:UUID
    content:str
    views:int
    post_type:str
    visible:bool
    user_id:UUID
    medias:List["MediaResponse"]
    post_comments:List["CommentResponse"]
    post_liked_users:List["UserResponse"]



    # post_id = Column(String,unique=True,default=lambda:Base().get_unique_id())
    # content = Column(String)
    # views=Column(Integer,default=0)
    # user_id = Column(UUID(as_uuid=uu),ForeignKey('users.id'),nullable=True)
    # post_type = Column(String)
    # visible=Column(Boolean,default=True)

    # #relations

    # user = relationship("UserModel",back_populates='posts')
    # comments = relationship("CommentModel",secondary=post_comments,back_populates="post",lazy=True)
    # medias = relationship("MediaModel",secondary=post_medias,back_populates="post",lazy=True)
    # post_liked_users = relationship("UsersModel",secondary=post_liked_user,back_populates="post_likes",lazy=True)
