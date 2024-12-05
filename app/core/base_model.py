from pickle import TRUE
from sqlmodel import SQLModel , Field
from uuid import UUID,uuid4
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import Column,DateTime
import secrets
import string
from sqlalchemy import UUID as SQL_UUID


class BaseModel(SQLModel):
    __abstract__=True

    id: UUID  = Field(
        default_factory=uuid4,
        sa_column=Column(SQL_UUID(as_uuid=uuid4),default=uuid4,primary_key=True,index=True)
    )
    created_at: datetime = Field(
        sa_column=Column(DateTime,default=func.now(),nullable=True)
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime,default=func.now(),nullable=True,onupdate=func.now())
    )

    @staticmethod
    def get_uid(length:int=12):
        ''.join(secrets.choice(string.ascii_letters+string.digits) for _ in range(length))
