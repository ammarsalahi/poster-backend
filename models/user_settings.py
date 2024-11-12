from db import Base
from sqlalchemy import Column,String,Boolean,Integer,ForeignKey
from sqlalchemy.orm import relationship
import random
import string

class UserSettings(Base):

    __tablename__="user_settings"

    theme=Column(String,default="dark")
    is_to_factor_authectication=Column(Boolean,default=False)
    otp_qrcode_image=Column(String,nullable=True)
    user_id = Column(UUID(as_uuid=uuid4),ForeignKey('users.id'),nullable=True)


    #relations
    user=relationship("UserModel",back_populates="settings")
