from app.core import Base
from sqlalchemy import Column,String,UUID,ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4

class NotificationModel(Base):
    __tablename__="notifications"

    action_type = Column(String)
    content_type = Column(String)
    state = Column(String,default="notcheck")
    user_id = Column(UUID(as_uuid=True),ForeignKey("users.id"))
    action_user_id = Column(UUID(as_uuid=True),ForeignKey("users.id"))

    user =  relationship("UserModel",foreign_keys=[user_id])
    action_user =  relationship("UserModel",foreign_keys=[action_user_id])
