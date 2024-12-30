from pydantic import BaseModel
from uuid import UUID

class NotificationAddSchema(BaseModel):
    action_type:str
    content_type:str
    user_id:UUID
    action_user_id:UUID

class NotificationEditSchema(BaseModel):
    action_type:str
    content_type:str
    user_id:UUID
    action_user_id:UUID
    state:str
