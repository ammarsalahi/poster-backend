from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr


class UserAddSchema(BaseModel):
    fullname:str
    username:str
    email:EmailStr
    password:str
    profile_type:Optional[str]
    profile_image:Optional[str]

class UserAddAdminSchema(BaseModel):
    fullname:str
    username:str
    email:EmailStr
    password:str
    profile_type:str|None=None


class UserEditSchema(BaseModel):
    username:str|None=None
    fullname:str|None=None
    email:EmailStr|None=None
    profile_type:str|None=None
    profile_image:str|None=None
    is_active:bool|None=None
    is_verified:bool|None=None


class UserEditAdminSchema(BaseModel):
    username:str|None=None
    fullname:str|None=None
    email:EmailStr|None=None
    profile_type:str|None=None
    profile_image:str|None=None
    is_active:bool|None=None
    is_verified:bool|None=None
    is_superuser:bool|None=None


class UserSigninSchema(BaseModel):
    username:str
    password:str

class UserTokenSchema(BaseModel):
    access_token:str

class UserPasswordChangeSchema(BaseModel):
    current_password:str
    new_password:str
