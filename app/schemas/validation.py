from pydantic import BaseModel,EmailStr

class ValidationAddSchema(BaseModel):
    email:EmailStr


class ValidationEditSchema(BaseModel):
    email:EmailStr
    is_verified:bool

class ValidationVerifySchema(BaseModel):
    email:EmailStr
    code:str