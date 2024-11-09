from db import Base
from sqlalchemy import Column,String,Boolean,Integer
import random
import string

class Story(Base):

    __tablename__="story"
   
    story_id = Column(String,unique=True,default=lambda:Base().get_unique_id(24))
    media = Column()
    replies=Column()
    views=Column(Integer,default=0)
    user = Column()
    liked_users=Column()
