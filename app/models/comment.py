from app.core import Base
from sqlalchemy import (
    UUID,
    Column,
    String,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from .table_relations import *


class CommentModel(Base):
    __tablename__ = "comments"

    content = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=False)
    visible = Column(Boolean, default=True)

    # Relationships with UserModel and PostModel
    user = relationship("UserModel", primaryjoin="CommentModel.user_id==UserModel.id",back_populates="user_comments")
    post = relationship("PostModel", primaryjoin="CommentModel.post_id==PostModel.id",back_populates="comments")

    liked_by = relationship("UserModel",secondary=liked_comments_table,back_populates="liked_comments")
