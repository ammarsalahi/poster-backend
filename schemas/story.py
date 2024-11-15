from pydantic import BaseModel,ConfigDict
from uuid import UUID,uuid4
from typing import List
from .user import UserResultSchema

class StorySchema(BaseModel):

    id:UUID
    story_id:str
    views:int
    user_id:UUID
    media_id:UUID
    created_at:str
    updated_at:str
    story_liked_users:List[UserResultSchema]|None

    model_config=ConfigDict(
        from_attributes=True
    )


class StoryCreateSchema(BaseModel):
    user_id:UUID
    media:str
    
    model_config=ConfigDict(
        from_attributes=True
    )


class StoryResultSchema(BaseModel):

    id:UUID
    story_id:str
    views:int
    user_id:UUID
    media:str
    created_at:str
    updated_at:str

    model_config=ConfigDict(
        from_attributes=True
    )

class StoryUpdateSchema(BaseModel):
    pass

    model_config=ConfigDict(
        from_attributes=True
    )

# class UserResultSchema(BaseModel):
#     id:UUID
#     story_id:str
#     views:int
#     user_id:UUID
#     media_id:UUID
#     created_at:str
#     updated_at:str

#     model_config=ConfigDict(
#         from_attributes=True
#     )



# class User(UserBase):
#     id:int

#     class Config:
#         orm_mode=True