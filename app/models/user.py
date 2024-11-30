from core import BaseModel
from uuid import UUID,uuid4
from sqlmodel import Field,Relationship,SQLModel
from datetime import datetime
from typing import List
from .linked_tables import *
from datetime import datetime
from .post import PostResponse
from .comment import CommentResponse
from .story import StoryResponse

class User(BaseModel,SQLModel,table=True):

    username:str = Field(unique=True,index=True,max_length=100)
    fullname:str = Field(max_length=200)
    email:str = Field(unique=True,max_length=300)
    password:str 
    last_login:datetime|None=None
    is_active:bool = Field(default=False)
    is_verified:bool = Field(default=False)
    is_superuser:bool = Field(default=False)
    profile_image_url:str | None = None
    profile_type:str | None = None
    #relations
    user_posts:List["Post"]= Relationship(back_populates='user')
    user_comments:List["Comment"] = Relationship(back_populates='user')
    stories:List["Story"]= Relationship(back_populates='user')
    liked_comments:List["Comment"] = Relationship(back_populates='comment_liked_users',link_model=UserCommentLink)
    liked_posts:List["Post"] = Relationship(back_populates="post_liked_users",link_model=UserPostLink)
    liked_stories:List["Story"] = Relationship(back_populates='story_liked_users',link_model=UserStoryLink)



class UserAdd(SQLModel):
    fullname:str =Field(max_length=100)
    username:str =Field(max_length=100)
    email:str
    password:str 
    profile_type:str|None



class UserEdit(SQLModel):
    username:str|None=None
    fullname:str|None=None
    email:str|None=None
    profile_type:str|None=None
    profile_image_url:str|None=None
    last_login:datetime|None=None
    is_active:bool|None=None
    is_verified:bool|None=None

class UserResponse(SQLModel):
    id:UUID
    username:str 
    fullname:str 
    email:str
    profile_type:str
    profile_image_url:str 
    last_login:datetime
    is_active:bool
    is_verified:bool
    is_superuser:bool
    created_at:datetime
    updated_at:datetime
    user_posts:List[PostResponse]
    user_comments:List[CommentResponse]
    user_stories:List[StoryResponse]
    liked_posts:List[PostResponse]
    liked_comments:List[CommentResponse]
    liked_stories:List[StoryResponse]

    

    

    





# class UserModel(Base):

#     __tablename__="users"

#     username = Column(String,unique=True,index=True)
#     fullname = Column(String)
#     email = Column(String,unique=True)
#     password = Column(String)
#     last_login = Column(DateTime)
#     is_active = Column(Boolean,default=False)
#     is_verified = Column(Boolean,default=False)
#     is_superuser = Column(Boolean,default=False)
#     profile_image=Column(String,nullable=True)
#     profile_type=Column(String,default="public")
    

#     #relations
#     setting=relationship("SettingModel",back_populates='user')
#     posts = relationship("PostModel",secondary=user_posts,back_populates="user",lazy=True)
#     comments=relationship("CommentModel",secondary=user_comments,back_populates="user",lazy=True)
#     stories=relationship("CommentModel",secondary=user_comments,back_populates="user",lazy=True)

#     post_likes = relationship("UserModel",back_populates="post_liked_users")
#     comment_likes = relationship("UserModel",back_populates="comment_liked_users")



