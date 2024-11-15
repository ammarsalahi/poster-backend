from db import Base
from sqlalchemy import Column,String,Boolean,Integer,ForeignKey,UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
import random
import string


class MediaModel(Base):

    __tablename__="media"
    
    media_file = Column(String)
    post_id = Column(UUID(as_uuid=uuid4),ForeignKey('posts.id'),nullable=True)
    post = relationship('PostModel',back_populates="medias")
