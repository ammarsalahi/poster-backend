from db import Base
from sqlalchemy import Column,String,Boolean,DateTime
from uuid import UUID,uuid4

class User(Base):

    __tablename__="users"

    username = Column(String,unique=True,index=True)
    fullname = Column(String)
    email = Column(String,unique=True)
    password = Column(String)
    last_login = Column(DateTime)
    is_active = Column(Boolean,default=False)
    is_verified = Column(Boolean,default=False)
    is_superuser = Column(Boolean,default=False)
    profile_image=Column()
    profile_type=Column(String)
