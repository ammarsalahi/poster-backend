from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,or_
from fastapi import HTTPException,status
from uuid import UUID
from models import *

class CommentCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int,is_superuser:bool):
        if is_superuser:
            query=select(Comment).offset(offset).limit(limit)
            async with self.db_session as session:
                comments= await session.execute(query)
                return comments.scalars()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            
    # async def filter(self,limit:int,offset:int,query:str):
    #     pass  
    async def read_one(self,comment_id:UUID):
        query=select(Comment).filter(Comment.id==comment_id)
        async with self.db_session as session: 
            comment=await session.execute(query)
            if comment:
                return comment.scalar()
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    async def add(self,comment_data:CommentAdd):
        comment=Comment(**comment_data.dict())
        async with self.db_session as session:
            session.add(comment)
            await session.commit()
        return comment

    async def update(self,comment_id:UUID,comment_data:CommentEdit):
        query=select(Comment).filter(Comment.id==comment_id)
        try:
            async with self.db_session as session:
                comment=session.execute(session)
                if comment:
                    for key , value in comment_data.dict(exclude_unset=True).items():
                        setattr(comment,key,value)
                    await session.commit()
                    return comment_data
                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)   

        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,comment_id:UUID):
        query=select(Commen).filter(Comment.id==comment_id)
        async with self.db_session as session:
            comment=await session.execute(query)
            if comment:
                await session.delete(comment)
                await session.commit()
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


