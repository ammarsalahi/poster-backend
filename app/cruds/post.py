from fastapi import HTTPException,status
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from utils.uid_tool import get_uid
from schemas.post import *
from models import *
from schemas.response import *
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
        query=sql.select(PostModel).filter(PostModel.post_id==post_id)
        async with self.db_session as session:
            try:
                post=await session.execute(query)
                if not post:
                    raise HTTPException(detail="Post Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return post.unique().scalar_one()
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
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,id:UUID):
        query=sql.select(PostModel).filter(PostModel.id==id)
        async with self.db_session as session:
            post=await session.execute(query)
            if post:
                await session.delete(post)
                await session.commit()
            else:
                raise HTTPException(detail="Post Not Found!",status_code=status.HTTP_404_NOT_FOUND)
