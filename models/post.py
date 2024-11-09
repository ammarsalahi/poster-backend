from db import Base
from sqlalchemy import Column,String,Boolean,Integer
import random
import string

class Post(Base):

    __tablename__="posts"
    
   
    post_id = Column(String,unique=True,default=lambda:Base().get_unique_id())
    content = Column(String)
    media = Column()
    interactions=Column()
    comments=Column()
    views=Column(Integer,default=0)
    user = Column()
    liked_users=Column()
    post_type = Column(String)
