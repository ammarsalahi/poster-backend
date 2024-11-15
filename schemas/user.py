from pydantic import BaseModel,ConfigDict
from uuid import UUID,uuid4
from datetime import datetime
from typing import List 
from .post import PostSchema
from .story import StoryResultSchema
class UserSchema(BaseModel):

    id:UUID
    username:str
    fullname:str
    email:str
    password:str
    profile_image:str
    profile_type:str
    created_at:datetime
    updated_at:datetime
    last_login:str
    is_active:bool
    is_superuser:bool
    is_verified:bool
    posts:List[PostSchema]|None
    stories:List[StoryResultSchema]|None


    model_config=ConfigDict(
        from_attributes=True
    )


class UserCreateSchema(BaseModel):
    username:str
    fullname:str
    email:str
    password:str
    profile_image:str|None=None
    profile_type:str|None=None
    
    model_config=ConfigDict(
        from_attributes=True
    )


class UserUpdateSchema(BaseModel):
    username:str|None=None
    fullname:str|None=None
    email:str|None=None
    password:str|None=None
    profile_image:str|None=None
    profile_type:str|None=None
    last_login:str|None=None
    is_active:bool|None=None
    is_superuser:bool|None=None
    is_verified:bool|None=None

    model_config=ConfigDict(
        from_attributes=True
    )

class UserResultSchema(BaseModel):
    id:UUID
    username:str
    fullname:str
    email:str
    profile_image:str
    profile_type:str
    created_at:datetime
    updated_at:datetime
    last_login:str
    is_active:bool
    is_superuser:bool
    is_verified:bool

    model_config=ConfigDict(
        from_attributes=True
    )

class PasswordSchema(BaseModel):
    old_password:str 
    new_password:str   


# class User(UserBase):
#     id:int

#     class Config:
#         orm_mode=True