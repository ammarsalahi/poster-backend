import uuid
from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.core import Base


class MediaModel(Base):
    __tablename__ = "medias"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    media_file = Column(String, nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=False)
    post = relationship("PostModel", back_populates="medias")
