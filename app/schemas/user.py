from datetime import datetime
from pydantic import BaseModel


class UserAddSchema(BaseModel):
    fullname:str
    username:str
    email:str
    password:str
    profile_type:str|None=None
    profile_image:str|None=None



class UserEditSchema(BaseModel):
    username:str|None=None
    fullname:str|None=None
    email:str|None=None
    profile_type:str|None=None
    profile_image:str|None=None
    is_active:bool|None=None
    is_verified:bool|None=None

class UserSigninSchema(BaseModel):
    username:str
    password:str

class UserTokenSchema(BaseModel):
    access_token:str

class UserPasswordChangeSchema(BaseModel):
    current_password:str
    new_password:str

