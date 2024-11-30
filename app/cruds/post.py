from sqlmodel.ext.asyncio import AsyncSession
from sqlmodel import select,or_
from fastapi import HTTPException,status
from typing import List
from uuid import UUID
from models import *

class PostCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int,is_superuser:bool):
        if is_superuser:
            query=select(Post).offset(offset).limit(limit)
            async with self.db_session as session:
                posts= await session.execute(query)
                return posts.scalars()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            
    async def filter(self,limit:int,offset:int,query:str):
        pass  

    async def read_one(self,id:UUID):
        query=select(Post).filter(Post.id==id)
        async with self.db_session as session: 
            post=await session.execute(query)
            if post:
                return post.scalar()
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    async def read_by_post_id(self,post_id:str):
        query=select(Post).filter(Post.post_id==post_id)
        async with self.db_session as session: 
            post=await session.execute(query)
            if post:
                return post.scalar()
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    async def add(self,post_data:PostAdd):
        post=Post(**post_data.dict())
        async with self.db_session as session:
            session.add(post)
            await session.commit()
        return post

    async def update(self,post_id:UUID,post_data:PostEdit):
        query=select(Post).filter(Post.post_id==post_id)
        try:
            async with self.db_session as session:
                post=session.execute(session)
                if post:
                    for key , value in post_data.dict(exclude_unset=True).items():
                        setattr(post,key,value)
                    await session.commit()
                    return post
                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)   

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
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) 

