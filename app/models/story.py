from db import BaseModel
from sqlmodel import Field,Relationship,SQLModel
import random
import string
from uuid import uuid4,UUID
from typing import List
from .linked_tables import *
from datetime import datetime
from .user import UserResponse


class Story(SQLModel,table=True):
    story_id:str = Field(unique=True,default=lambda:BaseModel().get_uid(20))
    views:int = Field(default=0,min_items=0)
    media_file:str | None = None
    story_type:str = Field()
    user_id:UUID | None = Field(default=None,foreign_key="user.id")
    user:"User" = Relationship(back_populates='stories')
    story_liked_users:List["User"] =Relationship(back_populates='liked_stories',link_model=UserStoryLink)
    

class StoryAdd(SQLModel):
    media_file:str 
    user_id:UUID
    sorty_type:str|None=None

class StoryEdit(SQLModel):
    media_file:str|None=None
    sorty_type:str|None=None

class StoryResponse(SQLModel):
    id:UUID
    story_id:str
    media_file:str
    views:int   
    user_id:UUID
    created_at:datetime
    updated_at:datetime 
    story_liked_users:List[str]





    # __tablename__="stories"
   
    # story_id = Column(String,unique=True,default=lambda:Base().get_unique_id(24))
    # # replies=Column()
    # views=Column(Integer,default=0)
    # user_id = Column(UUID(as_uuid=uuid4),ForeignKey('users.id'),nullable=True)
    # media_id= Column(UUID(as_uuid=uuid4),ForeignKey('media.id'),nullable=True)


    # #relations
    # media=relationship("MediaModel",back_populates="story")
    # user=relationship("UserModel",back_populates="stories")
    # story_liked_users = relationship("UsersModel",secondary=post_liked_user,back_populates="post_likes",lazy=True)
    # # medias = relationship("MediaModel",secondary=post_medias,back_populates="post",lazy=True)

 

