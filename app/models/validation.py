import uuid
from sqlalchemy import Column, String, Boolean, UUID
from sqlalchemy.ext.declarative import declarative_base
from app.core import Base
from app.utils.uid_tool import get_code_number
class ValidationModel(Base):
    __tablename__ = "validations"

    email = Column(String, nullable=False)
    code = Column(String,unique=True,default=get_code_number)
    is_verified = Column(Boolean, default=False)
