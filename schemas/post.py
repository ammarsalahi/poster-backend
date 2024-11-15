from pydantic import BaseModel,ConfigDict
from uuid import UUID,uuid4
from .comment import CommentSchema
from typing import List
class PostSchema(BaseModel):

    id:UUID
    post_id:str
    views:int 
    content:str
    user_id:UUID
    post_type:str 
    visible:bool
    created_at:str
    updated_at:str
    comments:List[CommentSchema]|None
    
    # terminals:List[TerminalSchema]|None
    # tickets:List[TerminalSchema]|None
    model_config=ConfigDict(
        from_attributes=True
    )


class PostCreateSchema(BaseModel):
    content:str
    user_id:UUID
    post_type:str 
    
    model_config=ConfigDict(
        from_attributes=True
    )


class PostUpdateSchema(BaseModel):
    views:int|None=None
    content:str|None=None
    post_type:str|None=None
    visible:bool|None=None

    model_config=ConfigDict(
        from_attributes=True
    )

# class PostResultSchema(BaseModel):
    

#     model_config=ConfigDict(
#         from_attributes=True
#     )


# class Post(PostBase):
#     id:int

#     class Config:
#         orm_mode=True