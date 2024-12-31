from app.core import Base
from sqlalchemy import Column,String,UUID,ForeignKey,Boolean
from sqlalchemy.orm import relationship
from uuid import uuid4

# class MessageModel(Base):
#     __tablename__="messages"

#     content  = Column(String)
#     state = Column(String,default="notchecked")
#     # relations
#     # IMAGES ADD MAYBE
#     parent_id = Column(UUID(as_uuid=True),ForeignKey("messages.id"),nullable=True)
#     send_user_id = Column(UUID(as_uuid=True),ForeignKey("users.id"))
#     recieve_user_id = Column(UUID(as_uuid=True),ForeignKey("users.id"))

#     parent = relationship("MessageModel",remote_side=[Base.id],back_populates="replies")
#     send_user =  relationship("UserModel",primaryjoin="MessageModel.send_user_id==UserModel.id",back_populates="user_sends")
#     recieve_user =  relationship("UserModel",primaryjoin="MessageModel.recieve_user_id==UserModel.id",back_populates="user_recieves")

class MessageModel(Base):
    __tablename__ = "messages"

    content = Column(String, nullable=False)  
    state = Column(String, default="notchecked")
    
    # Relations
    parent_id = Column(UUID(as_uuid=True), ForeignKey("messages.id"), nullable=True)
    send_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    recieve_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    # Self-referential relationship
    parent = relationship(
        "MessageModel",
        remote_side="MessageModel.id",  
        back_populates="replies",
    )
    replies = relationship(
        "MessageModel",
        back_populates="parent",
        cascade="all, delete-orphan",  
    )

    # User relationships
    send_user = relationship(
        "UserModel",
        primaryjoin="MessageModel.send_user_id == UserModel.id",
        back_populates="user_sends",
    )
    recieve_user = relationship(
        "UserModel",
        primaryjoin="MessageModel.recieve_user_id == UserModel.id",
        back_populates="user_recieves",
    )
