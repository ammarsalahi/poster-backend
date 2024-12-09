from sqlmodel import Field,SQLModel
import random
import string
from uuid import UUID,uuid4
from datetime import datetime
from sqlalchemy import Column,DateTime
from sqlalchemy.sql import func


class Settings(SQLModel,table=True):

    id: UUID  = Field(default_factory=uuid4,primary_key=True,index=True)
    theme:str = Field(default='dark')
    is_two_factor_auth:bool = Field(default=False)
    otp_qrcode_image:str|None = None
    user_id:UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(sa_column=Column(DateTime,default=func.now(),nullable=True))
    updated_at: datetime = Field(sa_column=Column(DateTime,default=func.now(),nullable=True,onupdate=func.now()))

class SettingsAdd(SQLModel):
    user_id:UUID
    them:str
    is_two_factor_auth:bool

class SettingsEdit(SQLModel):
    theme:str
    is_two_factor_auth:bool


class SettingsResponse(SQLModel):
    id:UUID
    user_id:UUID
    theme:str
    is_two_factor_auth:bool
    otp_qrcode_image:str
    created_at:datetime
    updated_at:datetime




# class UserSettingsModel(Base):

#     __tablename__="user_settings"

#     theme=Column(String,default="dark")
#     is_to_factor_authectication=Column(Boolean,default=False)
#     otp_qrcode_image=Column(String,nullable=True)
#     user_id = Column(UUID(as_uuid=uuid4),ForeignKey('users.id'),nullable=True)


#     #relations
#     user=relationship("UserModel",back_populates="settings")
