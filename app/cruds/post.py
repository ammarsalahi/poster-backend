from fastapi import HTTPException,status
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from app.utils.uid_tool import get_uid
from app.schemas.post import *
from app.models import *
from app.schemas.response import *
import sqlalchemy as sql


class PostCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int):
        query=sql.select(PostModel).options(
            selectinload(PostModel.medias),
            selectinload(PostModel.liked_by),
            selectinload(PostModel.comments)
        ).offset(offset).limit(limit)
        async with self.db_session as session:
            posts= await session.execute(query)
            return posts.unique().scalars()


    # async def filter(self,limit:int,offset:int,query:str):
    #     pass

    async def read_one(self,id:UUID):
        query=sql.select(PostModel).options(
            selectinload(PostModel.medias),
            selectinload(PostModel.liked_by),
            selectinload(PostModel.comments)
        ).filter(PostModel.id==id)
        async with self.db_session as session:
            try:
                post=await session.execute(query)
                if not post:
                    raise HTTPException(detail="Post Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return post.unique().scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    async def read_by_post_id(self,post_id:str):
        query=sql.select(PostModel).options(
            selectinload(PostModel.medias),
            selectinload(PostModel.liked_by),
            selectinload(PostModel.comments)
        ).filter(PostModel.post_id==post_id)
        async with self.db_session as session:
            try:
                post=await session.execute(query)
                if not post:
                    raise HTTPException(detail="Post Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return post.unique().scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def read_by_user_id(self,user_id:UUID):
        query=sql.select(PostModel).options(
            selectinload(PostModel.medias),
            selectinload(PostModel.liked_by),
            selectinload(PostModel.comments)
        ).filter(PostModel.user_id==user_id)
        async with self.db_session as session:
            try:
                post=await session.execute(query)
                return post.unique().scalars()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    async def add(self,post_data:PostAddSchema,medias:List[str]):

        post=PostModel(**post_data.dict())
        async with self.db_session as session:
            try:
                session.add(post)
                await session.flush()
                for media_data in medias:
                    new_media = MediaModel(
                        media_file=media_data,
                        post_id=post.id
                    )
                    session.add(new_media)
                await session.commit()
                return post
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    async def update(self,post_id:str,post_data:PostEditSchema,medias:List[str]):
        query=sql.select(PostModel).filter(PostModel.post_id==post_id)
        try:
            async with self.db_session as session:
                result=await session.execute(query)
                post=result.scalar_one_or_none()
                if not post:
                    raise HTTPException(detail="Post Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                for key , value in post_data.dict(exclude_unset=True).items():
                    setattr(post,key,value)
                for media_data in medias:
                    new_media = MediaModel(
                        media_file=media_data,
                        post_id=post_id
                    )
                    session.add(new_media)
                await session.commit()
                return post

        except Exception as e:
            # await session.rollback()
            raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,id:UUID):
        query=sql.select(PostModel).filter(PostModel.id==id)
        async with self.db_session as session:
            post=await session.execute(query)
            if not post:
                raise HTTPException(detail="Post Not Found!",status_code=status.HTTP_404_NOT_FOUND)
            await session.delete(post)
            await session.commit()

    async def like_post(self,post_id:UUID,user_id:UUID):
        post_query = sql.select(PostModel).filter(PostModel.id==post_id)
        user_query=sql.select(UserModel).filter(UserModel.id==user_id)
        async with self.db_session as session:
            try:
                post_result= await session.execute(post_query)
                user_result= await session.execute(user_query)

                post = post_result.scalar_one_or_none()
                user = user_result.scalar_one_or_none()
                if not post:
                    raise HTTPException(detail="Post Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                post.liked_by.append(user)
                await session.commit()
                return {"message":"post liked successfully!"}
            except Exception as e:
                raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    async def unlike_post(self,post_id:UUID,user_id:UUID):
        post_query = sql.select(PostModel).filter(PostModel.id==post_id)
        user_query=sql.select(UserModel).filter(UserModel.id==user_id)
        async with self.db_session as session:
            try:
                post_result= await session.execute(post_query)
                user_result= await session.execute(user_query)

                post = post_result.scalar_one_or_none()
                user = user_result.scalar_one_or_none()
                if not post:
                    raise HTTPException(detail="Post Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                post.liked_by.remove(user)
                await session.commit()
                return {"message":"post unliked successfully!"}
            except Exception as e:
                raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def save_post(self,post_id:UUID,user_id:UUID):
        post_query = sql.select(PostModel).filter(PostModel.id==post_id)
        user_query=sql.select(UserModel).filter(UserModel.id==user_id)
        async with self.db_session as session:
            try:
                post_result= await session.execute(post_query)
                user_result= await session.execute(user_query)

                post = post_result.scalar_one_or_none()
                user = user_result.scalar_one_or_none()
                if not post:
                    raise HTTPException(detail="Post Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                post.saved_by.append(user)
                await session.commit()
                return {"message":"post saved successfully!"}
            except Exception as e:
                raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def unsave_post(self,post_id:UUID,user_id:UUID):
        post_query = sql.select(PostModel).filter(PostModel.id==post_id)
        user_query=sql.select(UserModel).filter(UserModel.id==user_id)
        async with self.db_session as session:
            try:
                post_result= await session.execute(post_query)
                user_result= await session.execute(user_query)

                post = post_result.scalar_one_or_none()
                user = user_result.scalar_one_or_none()
                if not post:
                    raise HTTPException(detail="Post Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                post.saved_by.remove(user)
                await session.commit()
                return {"message":"post unsaved successfully!"}
            except Exception as e:
                raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)