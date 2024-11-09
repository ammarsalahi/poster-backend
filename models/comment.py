from db import Base
from sqlalchemy import Column,String,Boolean,Integer
import random
import string

class Comment(Base):

    __tablename__="posts"
   
    content = Column(String)
    interactions=Column()
    replies=Column()
    user = Column()
    comment_type = Column(String)
