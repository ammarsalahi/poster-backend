from sqlalchemy import UUID, Boolean, Column, DateTime,Table,ForeignKey, String
from sqlalchemy.orm import relationship
from app.core import Base
from .table_relations import *


class UserModel(Base):
    __tablename__="users"

    fullname = Column(String,nullable=True)
    username = Column(String,unique=True,index=True)
    email = Column(String,unique=True)
    password = Column(String)
    last_login = Column(DateTime,nullable=True)
    is_active = Column(Boolean,default=False)
    is_verified = Column(Boolean,default=False)
    is_superuser = Column(Boolean,default=False)
    profile_image = Column(String,default="noimage")
    profile_type = Column(String,nullable=True,default="public")

    #relations

    followers = relationship("FollowModel", back_populates="following", foreign_keys="FollowModel.following_id")
    followings = relationship("FollowModel", back_populates="follower", foreign_keys="FollowModel.follower_id")
    settings = relationship("SettingsModel", back_populates="user")
    user_posts = relationship("PostModel", back_populates="user",lazy="select")
    user_comments = relationship("CommentModel", back_populates="user",lazy="select")
    user_stories = relationship("StoryModel", back_populates="user",lazy="select")

   #like relations
    liked_posts = relationship("PostModel",secondary=liked_posts_table,back_populates="liked_by",lazy="select")
    liked_stories = relationship("StoryModel",secondary=liked_stories_table,back_populates="liked_by",lazy="select")
    liked_comments = relationship("CommentModel",secondary=liked_comments_table,back_populates="liked_by",lazy="select")

    # saved relations
    saved_posts= relationship("PostModel",secondary=saved_posts_table,back_populates="saved_by",lazy="select")
    saved_stories = relationship("StoryModel",secondary=saved_stories_table,back_populates="saved_by",lazy="select")

    # notif relations
    user_notifications = relationship("NotificationModel",primaryjoin="UserModel.id == NotificationModel.user_id",back_populates="user",lazy="select")
    user_actions = relationship("NotificationModel",primaryjoin="UserModel.id == NotificationModel.action_user_id",back_populates="action_user",lazy="select")

    # message relations
    user_sends = relationship("MessageModel",primaryjoin="UserModel.id == MessageModel.send_user_id",back_populates="send_user",lazy="select")
    user_recieves = relationship("MessageModel",primaryjoin="UserModel.id == MessageModel.recieve_user_id",back_populates="recieve_user",lazy="select")
