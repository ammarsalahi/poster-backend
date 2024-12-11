import uuid
from sqlalchemy import Column, String, Boolean, UUID
from sqlalchemy.ext.declarative import declarative_base
from core import Base

class ValidationModel(Base):
    __tablename__ = "validations"
    
    email = Column(String, nullable=False)
    code = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
