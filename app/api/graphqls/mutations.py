import os
from typing import Optional
import strawberry
from cruds import *
from .types import *
from api.deps import *
from strawberry.types import Info
from models import *
from fastapi import UploadFile
from typing import List
from utils.media import save_graph_media
from strawberry.file_uploads import Upload
from schemas.post import *
from schemas.comment import *
from schemas.story import *

@strawberry.type
class Mutation:

    @strawberry.mutation
    async def creete_post(self,info:Info,post_data:PostAddInput,upload_files:List[Upload])->Optional[PostType]:

        current_user= await get_user(info)
        if current_user:
            session = get_session(info)
            medias:List[str]=[]
            for upload in upload_files:
                file_path = await save_graph_media(upload)
                medias.append(file_path)
            post_add=PostAddSchema(
                content=post_data.content,
                post_type=post_data.post_type,
                user_id=current_user.id,
            )

            post= await PostCrud(session).add(post_add,medias)
            return PostType(**post.dict())

    @strawberry.mutation
    async def update_post(self,info:Info,post_id:str,post_data:PostEditInput,media_files:List[Upload],comments_data:List[CommentAddInput])->Optional[PostType]:
        session = get_session(info)
        current_user= await get_user(info)
        post = await PostCrud(session).read_by_post_id(post_id)
        if current_user.is_superuser or current_user.id==post.user_id:
            medias:List[str]= []
            for media in media_files:
                file_path = await save_graph_media(media)
                medias.append(file_path)
            post_edit = PostEditSchema(
                content=post_data.content,
                post_type = post_data.post_type,
                views=post_data.views,
                visible=post_data.visible,
            )
            post = await PostCrud(session).update(post_id,post_edit,medias)
            return PostType(**post.dict())
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")


    @strawberry.mutation
    async def creete_comment(self,info:Info,comment_data:CommentAddInput)->Optional[CommentType]:
        current_user= await get_user(info)
        if current_user:
            session = get_session(info)
            comment_add=CommentAddSchema(
                content=comment_data.content,
                post_id=comment_data.post_id,
                user_id=current_user.id
            )
            comment= await CommentCrud(session).add(comment_add)
            return CommentType(**comment.dict())

    @strawberry.mutation
    async def update_comment(self,info:Info,comment_id:UUID,content:str)->Optional[CommentType]:
        session = get_session(info)
        current_user= await get_user(info)
        comment = await CommentCrud(session).read_one(comment_id)
        if current_user.is_superuser or current_user.id==comment.user_id:
            comment_data=CommentEditSchema(
                content=content
            )
            comment = await CommentCrud(session).update(comment_id,comment_data)
            return CommentType(**comment.dict())
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")

    @strawberry.mutation
    async def creete_story(self,info:Info,media_file:Upload,story_type:str|None=None)->Optional[StoryType]:
        current_user= await get_user(info)
        if current_user:
            session = get_session(info)
            file_path=await save_graph_media(media_file)
            story_add=StoryAddSchema(
                media_file=file_path,
                user_id=current_user.id,
                story_type=story_type
            )
            stroy= await StoryCrud(session).add(story_add)
            return StoryType(**stroy.dict())

    @strawberry.mutation
    async def update_story(self,info:Info,story_id:str,media_file:Upload,story_type:str|None=None)->Optional[StoryType]:
        session = get_session(info)
        current_user= await get_user(info)
        story = await StoryCrud(session).read_by_story_id(story_id)
        if current_user.is_superuser or current_user.id==story.user_id:
            file_path=await save_media(media_file)
            story_data=StoryEditSchema(
                media_file=file_path,
                story_type=story_type
            )
            story = await StoryCrud(session).update(story_id,story_data)
            return StoryType(**story.dict())
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Method Not Allowed")
