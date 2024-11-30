from core import BaseModel
from sqlmodel import Field,Relationship,SQLModel
from uuid import uuid4,UUID
import random
import string
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import Column,DateTime

class Media(BaseModel,SQLModel,table=True):
    media_file:str
    post_id:UUID |None = Field(default=None,foreign_key="post.id")
    post: "Post"= Relationship(back_populates='medias')


class MediaAdd(SQLModel):
    media_file:str 
    post_id:UUID|None=None

class MediaEdit(SQLModel):
    media_file:str 


class MediaResponse(SQLModel):
    id:UUID
    media_file:str 
    post_id:UUID
    created_at:datetime
    updated_at:datetime



   




    # __tablename__="media"
    
    # media_file = Column(String)
    # post_id = Column(UUID(as_uuid=uuid4),ForeignKey('posts.id'),nullable=True)
    # post = relationship('PostModel',back_populates="medias")
