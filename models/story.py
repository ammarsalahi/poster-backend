from db import Base
from sqlalchemy import Column,String,Boolean,Integer,ForeignKey,UUID
from sqlalchemy.orm import relationship
import random
import string
from uuid import uuid4

class Story(Base):

    __tablename__="stories"
   
    story_id = Column(String,unique=True,default=lambda:Base().get_unique_id(24))
    # replies=Column()
    views=Column(Integer,default=0)
    user_id = Column(UUID(as_uuid=uuid4),ForeignKey('users.id'),nullable=True)
    media_id= Column(UUID(as_uuid=uuid4),ForeignKey('media.id'),nullable=True)


    #relations
    media=relationship("MediaModel",back_populates="story")
    user=relationship("UserModel",back_populates="stories")
    story_liked_users = relationship("UsersModel",secondary=post_liked_user,back_populates="post_likes",lazy=True)
    # medias = relationship("MediaModel",secondary=post_medias,back_populates="post",lazy=True)

 

