from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class SettingAddSchema(BaseModel):
    user_id:UUID

class SettingEditSchema(BaseModel):
    theme:str 
    is_two_factor_auth:bool
    # otp_qrcode_image:Optional[str]

