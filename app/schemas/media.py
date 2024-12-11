from uuid import UUID
from pydantic import BaseModel


class MediaAddSchema(BaseModel):
    media_file:str
    post_id:UUID

class MediaEditSchema(BaseModel):
    media_file:str
