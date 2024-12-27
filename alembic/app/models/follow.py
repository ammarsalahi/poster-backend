from sqlalchemy.orm import relationship
from app.core import Base
from sqlalchemy import Column, ForeignKey, UUID
import uuid


class FollowModel(Base):
    __tablename__ = "follows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    follower_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    following_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    follower = relationship("UserModel", foreign_keys=[follower_id], back_populates="followings")
    following = relationship("UserModel", foreign_keys=[following_id], back_populates="followers")

# from sqlalchemy.orm import Session
# from fastapi import HTTPException
# from uuid import UUID

# def follow_user(db: Session, follower_id: UUID, following_id: UUID):
#     if follower_id == following_id:
#         raise HTTPException(status_code=400, detail="You cannot follow yourself.")

#     # Check if the follow relationship already exists
#     follow_instance = db.query(FollowModel).filter(
#         FollowModel.follower_id == follower_id,
#         FollowModel.following_id == following_id
#     ).first()

#     if follow_instance:
#         raise HTTPException(status_code=400, detail="Already following this user.")

#     follow_instance = FollowModel(follower_id=follower_id, following_id=following_id)
#     db.add(follow_instance)
#     db.commit()
#     db.refresh(follow_instance)

#     return follow_instance

# def unfollow_user(db: Session, follower_id: UUID, following_id: UUID):
#     follow_instance = db.query(FollowModel).filter(
#         FollowModel.follower_id == follower_id,
#         FollowModel.following_id == following_id
#     ).first()

#     if not follow_instance:
#         raise HTTPException(status_code=404, detail="Follow relationship not found.")

#     db.delete(follow_instance)
#     db.commit()
#     return {"detail": "Unfollowed successfully"}
