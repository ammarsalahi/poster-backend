from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,or_
from fastapi import HTTPException,status
from typing import List
from uuid import UUID
from models import *

class PostCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int)->List[PostResponse]:
        query=select(Post).offset(offset).limit(limit)
        async with self.db_session as session:
            posts= await session.execute(query)
            return posts.scalars()


    async def filter(self,limit:int,offset:int,query:str):
        pass

    async def read_one(self,id:UUID)-> PostResponse:
        query=select(Post).filter(Post.id==id)
        async with self.db_session as session:
            try:
                post=await session.execute(query)
                if not post:
                    raise HTTPException(detail="Post Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return post.scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    async def read_by_post_id(self,post_id:str)->PostResponse:
        query=select(Post).filter(Post.post_id==post_id)
        async with self.db_session as session:
            try:
                post=await session.execute(query)
                if not post:
                    raise HTTPException(detail="Post Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return post.scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def add(self,post_data:PostAdd)->PostResponse:
        post=Post(**post_data.dict())
        async with self.db_session as session:
            try:
                session.add(post)
                await session.commit()
                return PostResponse(**post.dict())
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    async def update(self,post_id:str,post_data:PostEdit)->PostResponse:
        query=select(Post).filter(Post.post_id==post_id)
        try:
            async with self.db_session as session:
                post=await session.execute(query)
                if not post:
                    raise HTTPException(detail="Post Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                for key , value in post_data.dict(exclude_unset=True).items():
                    setattr(post,key,value)
                await session.commit()
                return post.scalar_one()

        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,id:UUID):
        query=select(Post).filter(Post.id==id)
        async with self.db_session as session:
            post=await session.execute(query)
            if post:
                await session.delete(post)
                await session.commit()
            else:
                raise HTTPException(detail="Post Not Found!",status_code=status.HTTP_404_NOT_FOUND)
