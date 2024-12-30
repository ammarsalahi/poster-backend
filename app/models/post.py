from app.core import Base
from sqlalchemy import (
    UUID,
    Column,
    String,
    Integer,
    Boolean,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.utils.uid_tool import get_uid
from .table_relations import *


class PostModel(Base):
    __tablename__ = "posts"

    post_id = Column(String,index=True,unique=True,default=get_uid)
    content = Column(String, nullable=True)
    views = Column(Integer, default=0)
    post_type = Column(String,nullable=True,default="public")  # e.g., 'text', 'image', 'video'
    visible = Column(Boolean, default=True)
    #relations
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    user = relationship("UserModel" ,back_populates="user_posts")
    medias = relationship("MediaModel",back_populates="post",lazy="select")
    comments= relationship("CommentModel", back_populates="post",lazy="select")
    liked_by = relationship( "UserModel",secondary=liked_posts_table,back_populates="liked_posts")
    saved_by = relationship( "UserModel",secondary=saved_posts_table,back_populates="saved_posts")
