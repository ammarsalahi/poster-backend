import uuid
from sqlalchemy import Column, ForeignKey, String, Boolean, UUID
from sqlalchemy.orm import relationship
from app.core import Base


class SettingsModel(Base):
    __tablename__ = "settings"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    theme = Column(String, default="dark")
    is_two_factor_auth = Column(Boolean, default=False)
    otp_qrcode_image = Column(String, nullable=True)

    user = relationship("UserModel", back_populates="settings")
