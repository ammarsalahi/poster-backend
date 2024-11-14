from pydantic import BaseModel,ConfigDict
from uuid import UUID,uuid4
from typing import List

class UserBase(BaseModel):

    id:UUID
    story_id:str
    views:int
    user_id:UUID
    media_id:UUID
    created_at:str
    updated_at:str
    # story_liked_users:List[]|None

    # terminals:List[TerminalSchema]|None
    # tickets:List[TerminalSchema]|None
    model_config=ConfigDict(
        from_attributes=True
    )


class StoryCreate(BaseModel):
    pass
    
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