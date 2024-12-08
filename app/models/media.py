from sqlmodel import Field,Relationship,SQLModel
from uuid import uuid4,UUID
import random
import string
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import Column,DateTime

class Media(SQLModel,table=True):

    id: UUID  = Field(default_factory=uuid4,primary_key=True,index=True)
    media_file:str
    post_id:UUID = Field(foreign_key="post.id")
    user_id:UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(sa_column=Column(DateTime,default=func.now(),nullable=True))
    updated_at: datetime = Field(sa_column=Column(DateTime,default=func.now(),nullable=True,onupdate=func.now()))
    post: "Post"= Relationship(back_populates='medias')


class MediaAdd(SQLModel):
    media_file:str
    post_id:UUID
    user_id:UUID

class MediaEdit(SQLModel):
    media_file:str


class MediaResponse(SQLModel):
    id:UUID
    media_file:str
    post_id:UUID
    user_id:UUID
    created_at:datetime
    updated_at:datetime








    # __tablename__="media"

    # media_file = Column(String)
    # post_id = Column(UUID(as_uuid=uuid4),ForeignKey('posts.id'),nullable=True)
    # post = relationship('PostModel',back_populates="medias")
