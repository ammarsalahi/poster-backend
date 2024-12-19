from uuid import UUID
import strawberry
from .types import *
from app.api.deps import *
from app.cruds import *
from fastapi import HTTPException
from typing import List,Optional
from strawberry.types import Info


@strawberry.type
class Query:

    @strawberry.field
    async def filter_users(self,info:Info,q:str,limit:int=10 )->Optional[List[UserType]]:
        session = get_session(info)
        current_user = await get_user(info)
        if current_user:
            users= await UserCrud(session).filter(limit,q)
            return [UserType(**user.dict()) for user in users]

    @strawberry.field
    async def get_user(self,info:Info,username:str )->Optional[UserType]:
        session = get_session(info)
        current_user = await get_user(info)
        if current_user:
            user= await UserCrud(session).read_by_username(username)
            if not user:
                raise HTTPException(detail="User Not Found",status_code=status.HTTP_404_NOT_FOUND)
            return UserType(**user.dict())

    @strawberry.field
    async def get_posts(self,info:Info,limit:int=10,offset:int=0 )->Optional[List[PostType]]:
        session = get_session(info)
        current_user = await get_user(info)
        if current_user:
            posts= await PostCrud(session).read_all(limit,offset)
            return [PostType(**post.dict()) for post in posts]

    @strawberry.field
    async def get_post(self,info:Info,post_id:str )->Optional[PostType]:
        session = get_session(info)
        current_user = await get_user(info)
        if current_user:
            user= await PostCrud(session).read_by_post_id(post_id)
            if not user:
                raise HTTPException(detail="Post Not Found",status_code=status.HTTP_404_NOT_FOUND)
            return PostType(**user.dict())

    @strawberry.field
    async def get_stories(self,info:Info,limit:int=10,offset:int=0 )->Optional[List[StoryType]]:
        session = get_session(info)
        current_user = await get_user(info)
        if current_user:
            stories= await StoryCrud(session).read_all(limit,offset)
            return [StoryType(**story.dict()) for story in stories]

    @strawberry.field
    async def get_story(self,info:Info,story_id:str )->Optional[StoryType]:
        session = get_session(info)
        current_user = await get_user(info)
        if current_user:
            story= await StoryCrud(session).read_by_story_id(story_id)
            if not story:
                raise HTTPException(detail="Story Not Found",status_code=status.HTTP_404_NOT_FOUND)
            return StoryType(**story.dict())

    @strawberry.field
    async def get_comments(self,info:Info,limit:int=10,offset:int=0 )->Optional[List[CommentType]]:
        session = get_session(info)
        current_user = await get_user(info)
        if current_user:
            comments= await CommentCrud(session).read_all(limit,offset)
            return [CommentType(**comment.dict()) for comment in comments]

    @strawberry.field
    async def get_comment(self,info:Info,id:UUID )->Optional[CommentType]:
        session = get_session(info)
        current_user = await get_user(info)
        if current_user:
            story= await CommentCrud(session).read_one(id)
            if not story:
                raise HTTPException(detail="Comment Not Found",status_code=status.HTTP_404_NOT_FOUND)
            return CommentType(**story.dict())
