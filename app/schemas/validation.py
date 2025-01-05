from pydantic import BaseModel,EmailStr

class ValidationAddSchema(BaseModel):
    email:str


class ValidationEditSchema(BaseModel):
    email:str
    is_verified:bool

class ValidationVerifySchema(BaseModel):
    email:str
    code:str