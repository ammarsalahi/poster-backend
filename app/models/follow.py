from sqlalchemy.orm import relationship
from core import Base
from sqlalchemy import Column, ForeignKey, UUID
import uuid


class FollowModel(Base):
    __tablename__ = "follows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    follower_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    following_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    follower = relationship("UserModel", foreign_keys=[follower_id], back_populates="followings")
    following = relationship("UserModel", foreign_keys=[following_id], back_populates="followers")
