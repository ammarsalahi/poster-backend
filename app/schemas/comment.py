from pydantic import BaseModel
from uuid import UUID

class CommentAddSchema(BaseModel):
    content:str
    post_id:UUID
    user_id:UUID

class CommentEditSchema(BaseModel):
    content:str
