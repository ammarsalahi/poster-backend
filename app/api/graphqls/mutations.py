import strawberry
from cruds import *
from .types import *
from models import *
from api.deps import *

@strawberry.type
class Mutation:

    @strawberry.mutation
    async def creete_post(self,session:sessionDep,currentUser:userDep,post_data:PostAdd)->PostType:
        if currentUser:
            post= await PostCrud(session).add(post_data)
            return PostType(**post.dict())

    @strawberry.mutation
    async def update_post(self,session:sessionDep,currentUser:userDep,post_id:str,post_data:PostEdit)->PostType:
        post = await PostCrud(session).read_by_post_id(post_id)
        if currentUser.is_superuser or currentUser.id==post.user_id:
            post = await PostCrud(session).update(post_id,post_data)
            return PostType(**post.dict())
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


    @strawberry.mutation
    async def creete_comment(self,session:sessionDep,currentUser:userDep,comment_data:CommentAdd)->CommentType:
        if currentUser:
            comment= await CommentCrud(session).add(comment_data)
            return CommentType(**comment.dict())

    @strawberry.mutation
    async def update_comment(self,session:sessionDep,currentUser:userDep,comment_id:UUID,comment_data:CommentEdit)->CommentType:
        comment = await CommentCrud(session).read_one(comment_id)
        if currentUser.is_superuser or currentUser.id==comment.user_id:
            comment = await CommentCrud(session).update(comment_id,comment_data)
            return CommentType(**comment.dict())
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

    @strawberry.mutation
    async def creete_story(self,session:sessionDep,currentUser:userDep,stroy_data:StoryAdd)->StoryType:
        if currentUser:
            stroy= await StoryCrud(session).add(stroy_data)
            return StoryType(**stroy.dict())

    @strawberry.mutation
    async def update_story(self,session:sessionDep,currentUser:userDep,story_id:str,stroy_data:StoryEdit)->StoryType:
        story = await StoryCrud(session).read_by_story_id(story_id)
        if currentUser.is_superuser or currentUser.id==story.user_id:
            story = await StoryCrud(session).update(story_id,stroy_data)
            return StoryType(**story.dict())
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")
