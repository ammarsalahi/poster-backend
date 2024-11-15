from pydantic import BaseModel,ConfigDict
from uuid import UUID,uuid4


class CommentSchema(BaseModel):

    id:UUID
    content:str
    user_id:UUID
    post_id:UUID 
    comment_type:str
    visible:bool
    created_at:str
    updated_at:str

    model_config=ConfigDict(
        from_attributes=True
    )


class CommentCreateSchema(BaseModel):
    content:str
    user_id:UUID
    post_id:UUID
    comment_type:str 
    
    model_config=ConfigDict(
        from_attributes=True
    )


class CommentUpdateSchema(BaseModel):
    content:str|None=None
    user_id:UUID|None=None
    post_id:UUID|None=None 
    comment_type:str|None=None
    visible:bool|None=None

    model_config=ConfigDict(
        from_attributes=True
    )

