from db import Base
from sqlalchemy import Column,String,Boolean,Integer,ForeignKey
from sqlalchemy.orm import relationship
import random
import string
from uuid import uuid4
from .relation_tables import *


class PostModel(Base):

    __tablename__="posts"
   
    post_id = Column(String,unique=True,default=lambda:Base().get_unique_id())
    content = Column(String)
    views=Column(Integer,default=0)
    user_id = Column(UUID(as_uuid=uu),ForeignKey('users.id'),nullable=True)
    post_type = Column(String)
    visible=Column(Boolean,default=True)

    #relations

    user = relationship("UserModel",back_populates='posts')
    comments = relationship("CommentModel",secondary=post_comments,back_populates="post",lazy=True)
    medias = relationship("MediaModel",secondary=post_medias,back_populates="post",lazy=True)
    post_liked_users = relationship("UsersModel",secondary=post_liked_user,back_populates="post_likes",lazy=True) 

