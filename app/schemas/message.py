from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class MessageAddSchema(BaseModel):
    content:str
    send_user_id:UUID
    recieve_user_id:UUID
    parent_id:Optional[UUID]

class MeessageEditSchema(BaseModel):
    content:str
    state:str
