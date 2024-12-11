
from fastapi import HTTPException,status
from uuid import UUID
from sqlalchemy.ext.asyncio.session import AsyncSession
from schemas.comment import *
from models import *
from schemas.response import *
import sqlalchemy as sql
from sqlalchemy.orm import selectinload


class FollowCrud:

    def __init__(self,db_session:AsyncSession):
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int):
        query=sql.select(FollowModel).offset(offset).limit(limit)
        async with self.db_session as session:
            follows= await session.execute(query)
            return follows.scalars()

    async def read_one(self,comment_id:UUID):
        query=sql.select(CommentModel).options(
            selectinload(CommentModel.liked_by)
        ).filter(CommentModel.id==comment_id)
        async with self.db_session as session:
            try:
                comment=await session.execute(query)
                if not comment:
                    raise HTTPException(detail="Comment Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return comment.scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    async def add(self,comment_data:CommentAddSchema):
        comment=CommentModel(**comment_data.dict())
        async with self.db_session as session:
            try:
                session.add(comment)
                await session.commit()
                return comment
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def update(self,comment_id:UUID,comment_data:CommentEditSchema):
        query=sql.select(CommentModel).filter(CommentModel.id==comment_id)
        try:
            async with self.db_session as session:
                result= await session.execute(query)
                comment = result.scalar_one_or_none()
                if not comment:
                    raise HTTPException(detail="Comment Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                for key , value in comment_data.dict(exclude_unset=True).items():
                    setattr(comment,key,value)
                    await session.commit()
                return comment
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,comment_id:UUID):
        query=sql.select(CommentModel).filter(CommentModel.id==comment_id)
        async with self.db_session as session:
            comment=await session.execute(query)
            if comment:
                await session.delete(comment)
                await session.commit()
            else:
                raise HTTPException(detail="Comment Not Found!",status_code=status.HTTP_404_NOT_FOUND)
