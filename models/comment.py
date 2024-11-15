from db import Base
from sqlalchemy import Column,String,Boolean,Integer,ForeignKey,UUID
from sqlalchemy.orm import relationship
import random
import string
from uuid import uuid4
from .relation_tables import *

class CommentModel(Base):

    __tablename__="comments"
   
    content = Column(String)
    user_id= Column(UUID(as_uuid=uuid4),ForeignKey('users.id'),nullable=True)
    post_id= Column(UUID(as_uuid=uuid4),ForeignKey('posts.id'),nullable=True)
    comment_type = Column(String)
    visible=Column(Boolean,default=True)

    #relations
    user=relationship("UserModel",back_populates="comments")
    post=relationship("PostModel",back_populates="comments")
    liked_users=relationship("UserModel",secondary=comment_liked_user,back_populates="comment_likes",lazy=True)



