from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import EmailStr
import strawberry


@strawberry.type
class MediaType:
    id:UUID
    media_file:str
    post_id:UUID
    user_id:UUID
    created_at:datetime
    updated_at:datetime


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
class UserType:
    id:UUID
    username:str
    fullname:str
    email:EmailStr
    profile_type:str
    profile_image_url:str
    last_login:datetime
    is_active:bool
    is_verified:bool
    is_superuser:bool
    created_at:datetime
    updated_at:datetime
    user_posts:List[PostType]
    user_comments:List[CommentType]
    user_stories:List[StoryType]
    liked_posts:List[PostType]
    liked_comments:List[CommentType]
    liked_stories:List[StoryType]
