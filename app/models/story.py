from app.utils.uid_tool import get_uid
from app.core import Base
from sqlalchemy import (
    UUID,
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .table_relations import *


class StoryModel(Base):
    __tablename__ = "stories"

    story_id = Column(String, unique=True, default=get_uid)
    media_file = Column(String, nullable=False)
    views = Column(Integer, default=0)
    story_type = Column(String,default="public")
    #relations
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("UserModel", back_populates="user_stories")
    liked_by = relationship("UserModel",secondary=liked_stories_table,back_populates="liked_stories")
    saved_by = relationship("UserModel",secondary=saved_stories_table,back_populates="saved_stories")
