from uuid import UUID
from pydantic import BaseModel


class StoryAddSchema(BaseModel):
    story_type:str
    user_id:UUID
    media_file:str

class StoryEditSchema(BaseModel):
    story_type:str
    media_file:str