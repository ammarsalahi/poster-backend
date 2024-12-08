from uuid import UUID
import strawberry
from .types import *
from api.deps import *
from cruds import *
from fastapi import HTTPException
from typing import List


@strawberry.type
class Query:

    @strawberry.field
    async def filter_users(self,session:sessionDep,q:str,limit:int=10 )->List[UserType]:
        users= await UserCrud(session).filter(limit,q)
        return [UserType(**user.dict()) for user in users]

    @strawberry.field
    async def get_user(self,session:sessionDep,username:str )->UserType:
        user= await UserCrud(session).read_by_username(username)
        if not user:
            raise HTTPException(detail="User Not Found",status_code=status.HTTP_404_NOT_FOUND)
        return UserType(**user.dict())

    @strawberry.field
    async def get_posts(self,session:sessionDep,limit:int=10,offset:int=0 )->List[PostType]:
        posts= await PostCrud(session).read_all(limit,offset)
        return [PostType(**post.dict()) for post in posts]

    @strawberry.field
    async def get_post(self,session:sessionDep,post_id:str )->PostType:
        user= await PostCrud(session).read_by_post_id(post_id)
        if not user:
            raise HTTPException(detail="Post Not Found",status_code=status.HTTP_404_NOT_FOUND)
        return PostType(**user.dict())

    @strawberry.field
    async def get_stories(self,session:sessionDep,limit:int=10,offset:int=0 )->List[StoryType]:
        stories= await StoryCrud(session).read_all(limit,offset)
        return [StoryType(**story.dict()) for story in stories]

    @strawberry.field
    async def get_story(self,session:sessionDep,story_id:str )->StoryType:
        story= await StoryCrud(session).read_by_story_id(story_id)
        if not story:
            raise HTTPException(detail="Story Not Found",status_code=status.HTTP_404_NOT_FOUND)
        return StoryType(**story.dict())

    @strawberry.field
    async def get_comments(self,session:sessionDep,limit:int=10,offset:int=0 )->List[CommentType]:
        comments= await CommentCrud(session).read_all(limit,offset)
        return [CommentType(**comment.dict()) for comment in comments]

    @strawberry.field
    async def get_comment(self,session:sessionDep,id:UUID )->CommentType:
        story= await CommentCrud(session).read_one(id)
        if not story:
            raise HTTPException(detail="Comment Not Found",status_code=status.HTTP_404_NOT_FOUND)
        return CommentType(**story.dict())
