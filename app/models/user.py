from uuid import UUID,uuid4
from sqlmodel import Field,Relationship,SQLModel
from datetime import datetime
from typing import List
from .linked_tables import *
from datetime import datetime
from sqlalchemy import Column,DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel



class User(SQLModel,table=True):

    id: UUID  = Field(default_factory=uuid4,primary_key=True,index=True)
    username:str = Field(unique=True,index=True,max_length=100)
    fullname:str = Field(max_length=200)
    email:str = Field(unique=True,max_length=300)
    password:str
    last_login:datetime|None=None
    is_active:bool = Field(default=False)
    is_verified:bool = Field(default=False)
    is_superuser:bool = Field(default=False)
    profile_image_url:str | None = None
    profile_type:str | None = None
    created_at: datetime = Field(sa_column=Column(DateTime,default=func.now(),nullable=True))
    updated_at: datetime = Field(sa_column=Column(DateTime,default=func.now(),nullable=True,onupdate=func.now()))
    #relations
    user_posts:List["Post"]= Relationship(back_populates='user')
    user_comments:List["Comment"] = Relationship(back_populates='user')
    stories:List["Story"]= Relationship(back_populates='user')
    liked_comments:List["Comment"] = Relationship(back_populates='comment_liked_users',link_model=UserCommentLink)
    liked_posts:List["Post"] = Relationship(back_populates="post_liked_users",link_model=UserPostLink)
    liked_stories:List["Story"] = Relationship(back_populates='story_liked_users',link_model=UserStoryLink)



class UserAdd(SQLModel):
    fullname:str =Field(max_length=100)
    username:str =Field(max_length=100)
    email:str
    password:str
    profile_type:str|None



class UserEdit(SQLModel):
    username:str|None=None
    fullname:str|None=None
    email:str|None=None
    profile_type:str|None=None
    profile_image_url:str|None=None
    last_login:datetime|None=None
    is_active:bool|None=None
    is_verified:bool|None=None

class UserSignin(SQLModel):
    username:str
    password:str

class UserToken(BaseModel):
    access_token:str

class UserPasswordChange(SQLModel):
    current_password:str
    new_password:str


class UserResponse(SQLModel):
    id:UUID
    username:str
    fullname:str
    email:str
    profile_type:str
    profile_image_url:str
    last_login:datetime
    is_active:bool
    is_verified:bool
    is_superuser:bool
    created_at:datetime
    updated_at:datetime
    user_posts:List["PostResponse"]
    user_comments:List["CommentResponse"]
    user_stories:List["StoryResponse"]
    liked_posts:List["PostResponse"]
    liked_comments:List["CommentResponse"]
    liked_stories:List["StoryResponse"]
