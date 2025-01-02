
from fastapi import HTTPException,status,Response
from uuid import UUID
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.comment import *
from app.models import *
from app.schemas.response import *
import sqlalchemy as sql
from sqlalchemy.orm import selectinload



class CommentCrud:

    def __init__(self,db_session:AsyncSession):
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int):
        query=sql.select(CommentModel).options(
            selectinload(CommentModel.liked_by)
        ).offset(offset).limit(limit)
        async with self.db_session as session:
            comments= await session.execute(query)
            return comments.unique().scalars()

    async def read_one(self,comment_id:UUID):
        query=sql.select(CommentModel).options(
            selectinload(CommentModel.liked_by)
        ).filter(CommentModel.id==comment_id)
        async with self.db_session as session:
            try:
                comment=await session.execute(query)
                return comment.unique().scalar_one()
            except sql.exc.NoResultFound:
                raise HTTPException(detail="Comment Not Found!",status_code=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def read_by_user_id(self,user_id:UUID):
        query=sql.select(CommentModel).options(
            selectinload(CommentModel.liked_by)
        ).filter(CommentModel.user_id==user_id)
        async with self.db_session as session:
            try:
                comment=await session.execute(query)
                return comment.unique().scalars()
            except sql.exc.NoResultFound:
                raise HTTPException(detail="Comments Not Found!",status_code=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def add(self,comment_data:CommentAddSchema):
        comment=CommentModel(**comment_data.model_dump())
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
                for key , value in comment_data.model_dump(exclude_unset=True).items():
                    setattr(comment,key,value)
                    await session.commit()
                return comment
        except sql.exc.NoResultFound:
                raise HTTPException(detail="Comment Not Found!",status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # await session.rollback()
            raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,comment_id:UUID):
        query=sql.select(CommentModel).filter(CommentModel.id==comment_id)
        async with self.db_session as session:
            try:
                result=await session.execute(query)
                comment = result.scalar_one_or_none()
                if not comment:
                    raise HTTPException(detail="Comment Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                await session.delete(comment)
                await session.commit()
                # return Response(status_code=status.HTTP_204_NO_CONTENT,content="comment delete successfully")
            except sql.exc.NoResultFound:
                raise HTTPException(detail="Comment Not Found!",status_code=status.HTTP_404_NOT_FOUND)

    async def like_comment(self,comment_id:UUID,user_id:UUID):
        comment_query = sql.select(CommentModel).filter(CommentModel.id==comment_id)
        user_query=sql.select(UserModel).filter(UserModel.id==user_id)
        async with self.db_session as session:
            try:
                comment_result= await session.execute(comment_query)
                user_result= await session.execute(user_query)

                comment = comment_result.scalar_one_or_none()
                user = user_result.scalar_one_or_none()
                if not comment:
                    raise HTTPException(detail="Comment Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                comment.liked_by.append(user)
                await session.commit()
                return {"message":"comment unliked successfully!"}

            except sql.exc.NoResultFound:
                raise HTTPException(detail="Comment Not Found!",status_code=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    async def unlike_comment(self,comment_id:UUID,user_id:UUID):
        comment_query = sql.select(CommentModel).filter(CommentModel.id==comment_id)
        user_query=sql.select(UserModel).filter(UserModel.id==user_id)
        async with self.db_session as session:
            try:
                comment_result= await session.execute(comment_query)
                user_result= await session.execute(user_query)

                comment = comment_result.scalar_one_or_none()
                user = user_result.scalar_one_or_none()
                if not comment:
                    raise HTTPException(detail="Comment Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                comment.liked_by.remove(user)
                await session.commit()
                return {"message":"comment unliked successfully!"}

            except sql.exc.NoResultFound:
                raise HTTPException(detail="Comment Not Found!",status_code=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
