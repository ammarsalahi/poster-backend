from db import Base
from sqlalchemy import Column,String,Boolean,Integer
import random
import string

class UserSettings(Base):

    __tablename__="posts"
    
   
    user=Column()
