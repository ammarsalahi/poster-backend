from sqlmodel import SQLModel,Field
from pydantic import EmailStr
from uuid import UUID,uuid4
from datetime import datetime
from sqlalchemy import Column,DateTime
from sqlalchemy.sql import func
import sqlmodel
from utils.uid_tool import get_code_number

class Validation(SQLModel,table=True):
    id: UUID  = Field(default_factory=uuid4,primary_key=True,index=True)
    email:EmailStr
    code:str = Field(unique=True,default=lambda:get_code_number(6))
    is_verified:bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(DateTime,default=func.now(),nullable=True))
    updated_at: datetime = Field(sa_column=Column(DateTime,default=func.now(),nullable=True,onupdate=func.now()))


class ValidationAdd(SQLModel):
    email:EmailStr

class ValidationCheck(SQLModel):
    email:EmailStr
    code:str

class ValidationEdit(SQLModel):
    is_verifiend:bool|None=None

class ValidationResponse(SQLModel):
    id: UUID
    email:EmailStr
    code:str
    is_verified:bool
    created_at: datetime
    updated_at: datetime
