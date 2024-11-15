from db import Base
from sqlalchemy import Column,String,Boolean,DateTime
from sqlalchemy.orm import relationship
from uuid import UUID,uuid4
from .relation_tables import *

class UserModel(Base):

    __tablename__="users"

    username = Column(String,unique=True,index=True)
    fullname = Column(String)
    email = Column(String,unique=True)
    password = Column(String)
    last_login = Column(DateTime)
    is_active = Column(Boolean,default=False)
    is_verified = Column(Boolean,default=False)
    is_superuser = Column(Boolean,default=False)
    profile_image=Column(String,nullable=True)
    profile_type=Column(String,default="public")
    

    #relations
    setting=relationship("SettingModel",back_populates='user')
    posts = relationship("PostModel",secondary=user_posts,back_populates="user",lazy=True)
    comments=relationship("CommentModel",secondary=user_comments,back_populates="user",lazy=True)
    stories=relationship("CommentModel",secondary=user_comments,back_populates="user",lazy=True)

    post_likes = relationship("UserModel",back_populates="post_liked_users")
    comment_likes = relationship("UserModel",back_populates="comment_liked_users")



