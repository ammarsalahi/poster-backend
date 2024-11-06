from pydantic import BaseModel

class UserBase(BaseModel):

    id:int
    personal_id:str
    fullname:str
    phone:str
    password:str
    created_at:str
    updated_at:str
    last_login:str
    is_active:bool
    is_superuser:bool


class UserCreate(BaseModel):
    personal_id:str
    fullname:str
    phone:str
    password:str

class User(UserBase):
    id:int

    class Config:
        orm_mode=True