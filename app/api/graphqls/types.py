from datetime import datetime
from typing import List
from typing_extensions import Optional
from uuid import UUID
from pydantic import EmailStr
import strawberry
from app.api.deps import sessionDep,userDep
from strawberry.types import Info
from fastapi import HTTPException,status
from app.models import *


def get_session(info: Info) -> sessionDep:
    return info.context["session"]

async def get_user(info: Info) -> userDep:
    current_user = info.context.get("current_user")
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    return current_user


#media Types
@strawberry.type
class MediaType:
    id:UUID
    media_file:str
    post_id:UUID
    user_id:UUID
    created_at:datetime
    updated_at:datetime



#post types
@strawberry.type
class PostType:
    post_id:UUID
    content:str
    views:int
    post_type:str
    visible:bool
    user_id:UUID
    medias:List[MediaType]
    post_comments:List["CommentType"]
    post_liked_users:List["UserType"]




#story types
@strawberry.type
class StoryType:
    id:UUID
    story_id:str
    media_file:str
    views:int
    user_id:UUID
    created_at:datetime
    updated_at:datetime
    story_liked_users:List["UserType"]



#comment types
@strawberry.type
class CommentType:
    id:UUID
    content:str
    user_id:UUID
    post_id:UUID
    created_at:datetime
    updated_at:datetime
    visible:bool
    comment_liked_users:List["UserType"]

@strawberry.type
class FollowType:
    id:UUID
    follower:UUID
    following:UUID

#user types
@strawberry.type
class UserType:
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
    followers:List[FollowType]
    followings:List[FollowType]
    user_posts:List[PostType]
    user_comments:List[CommentType]
    user_stories:List[StoryType]
    liked_posts:List[PostType]
    liked_comments:List[CommentType]
    liked_stories:List[StoryType]



#inputs

@strawberry.input
class PostAddInput:
    content:str|None
    post_type:str|None=None


@strawberry.input
class CommentAddInput:
    content:str
    post_id:UUID


@strawberry.input
class PostEditInput:
    content:str|None=None
    post_type:str|None=None
    views:int|None=None
    visible:bool|None=None
