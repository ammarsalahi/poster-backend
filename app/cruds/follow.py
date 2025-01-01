
from fastapi import HTTPException,status
from uuid import UUID
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.follow import *
from app.models import *
from app.schemas.response import *
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

    async def read_one(self,id:UUID):
        query=sql.select(FollowModel).filter(FollowModel.id==id)
        async with self.db_session as session:
            try:
                follow=await session.execute(query)
                return follow.scalar_one()
            except sql.exc.NoResultFound:
                raise HTTPException(detail="Follow Not Found!",status_code=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    async def add(self,data:FollowSchema):
        query= sql.select(FollowModel).filter(
            FollowModel.follower_id==data.follower_id,
            FollowModel.following_id==data.following_id,
        )
        follow = FollowModel(**data.model_dump())
        async with self.db_session as session:
            try:
                if data.follower_id==data.following_id:
                    raise HTTPException(detail="You can't follow yourself!",status_code=status.HTTP_400_BAD_REQUEST)
                follows=session.execute(query)
                if follows:
                    raise HTTPException(detail="Already following this user.",status_code=status.HTTP_400_BAD_REQUEST)
                else:
                    session.add(follow)
                    await session.commit()
                    return {"message":"User Successfully Followed"}

            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    async def remove(self,data:FollowSchema):
        query= sql.select(FollowModel).filter(
            FollowModel.follower_id==data.follower_id,
            FollowModel.following_id==data.following_id,
        )
        async with self.db_session as session:
            try:

                follow = await session.execute(query)
                await session.delete(follow)
                await session.commit()
                return {"message":"User Successfully Unfollowed"}
            except sql.exc.NoResultFound:
                raise HTTPException(detail="Follow Not Found!",status_code=status.HTTP_404_NOT_FOUND)
