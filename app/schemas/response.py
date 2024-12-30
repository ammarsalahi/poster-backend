from datetime import datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr


class FollowResponse(BaseModel):
    id:UUID
    follower_id:UUID
    following_id:UUID

class UserOnlyResponse(BaseModel):
    id:UUID
    username:str
    fullname:str
    email:str
    profile_type:str
    profile_image:str
    is_active:bool
    is_verified:bool
    is_superuser:bool
    created_at:datetime
    updated_at:datetime

class UserResponse(BaseModel):
    id:UUID
    username:str
    fullname:str
    email:str
    profile_type:str
    profile_image:str
    is_active:bool
    is_verified:bool
    is_superuser:bool
    created_at:datetime
    updated_at:datetime
    # user_posts:List["PostOnlyResponse"]
    # user_comments:List["CommentOnlyResponse"]
    # user_stories:List["StoryOnlyResponse"]
    # followers:List["FollowResponse"]
    # followings:List["FollowResponse"]
    # liked_posts:List["PostOnlyResponse"]
    # liked_comments:List["CommentOnlyResponse"]
    # liked_stories:List["StoryOnlyResponse"]


class SettingsResponse(BaseModel):
    id:UUID
    user_id:UUID
    theme:str
    is_two_factor_auth:bool
    otp_qrcode_image:str
    created_at:datetime
    updated_at:datetime


class MediaResponse(BaseModel):
    id:UUID
    post_id:UUID
    media_file:str
    created_at:datetime
    updated_at:datetime


class StoryOnlyResponse(BaseModel):
    id:UUID
    story_id:str
    media_file:str
    views:int
    user_id:UUID
    created_at:datetime
    updated_at:datetime

class StoryResponse(BaseModel):
    id:UUID
    story_id:str
    media_file:str
    views:int
    user_id:UUID
    created_at:datetime
    updated_at:datetime
    liked_by:List["UserResponse"]


class PostResponse(BaseModel):
    id:UUID
    post_id:str
    content:str
    views:int
    post_type:str
    visible:bool
    user_id:UUID
    medias:List["MediaResponse"]
    liked_by:List["UserOnlyResponse"]
    comments:List["CommentOnlyResponse"]
    # post_liked_users:List["UserResponse"]
    #
    # model_config=ConfigDict(
    #     from_attributes=True
    # )


class CommentOnlyResponse(BaseModel):
    id:UUID
    content:str
    user_id:UUID
    post_id:UUID
    created_at:datetime
    updated_at:datetime
    visible:bool

class CommentResponse(BaseModel):
    id:UUID
    content:str
    user_id:UUID
    post_id:UUID
    created_at:datetime
    updated_at:datetime
    visible:bool
    liked_by:List["UserResponse"]


class ValidationResponse(BaseModel):
    id: UUID
    email:EmailStr
    code:str
    is_verified:bool
    created_at: datetime
    updated_at: datetime

class NotificationResponse(BaseModel):
    action_type:str
    content_type:str
    user_id:UUID
    action_user_id:UUID
    state:str

class MessageResponse(BaseModel):
    content:str
    send_user_id:UUID
    recieve_user_id:UUID
    parent_id:UUID
    state:str
    replies:List["MessageResponse"]
