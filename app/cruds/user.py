from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from models import *
from fastapi import HTTPException,status
from uuid import UUID
from core.security import hashed_password,verify_password
from typing import List
from pydantic import EmailStr
from schemas.response import *
from schemas.user import *
import sqlalchemy as sql



class UserCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int,is_superuser:bool):
        if is_superuser:
            query=sql.select(UserModel).options(
                selectinload(UserModel.user_posts),
                selectinload(UserModel.user_comments),
                selectinload(UserModel.user_stories),
                selectinload(UserModel.liked_posts),
                selectinload(UserModel.liked_stories),
                selectinload(UserModel.liked_comments),
                selectinload(UserModel.followers),
                selectinload(UserModel.followings)
            ).offset(offset).limit(limit)
            async with self.db_session as session:
                try:
                    users = await session.execute(query)
                    return users.unique().scalars()
                except Exception as e:
                    raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    async def filter(self,limit:int,q:str):
        query=sql.select(UserModel).filter(
            sql.or_(
                UserModel.fullname.icontains==q,
                UserModel.username.icontains==q,
            )
        ).limit(limit)
        async with self.db_session as session:
            users=await session.execute(query)
            return users.unique().scalars()

    async def read_one(self,user_id:UUID):
        query=sql.select(UserModel).options(
            selectinload(UserModel.user_posts),
            selectinload(UserModel.user_comments),
            selectinload(UserModel.user_stories),
            selectinload(UserModel.liked_posts),
            selectinload(UserModel.liked_stories),
            selectinload(UserModel.liked_comments),
            selectinload(UserModel.followers),
            selectinload(UserModel.followings)
        ).filter(UserModel.id==user_id)
        async with self.db_session as session:
            try:
                user= await session.execute(query)
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return user.unique().scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def read_by_username(self,username:str):
        query=sql.select(UserModel).options(
            selectinload(UserModel.user_posts),
            selectinload(UserModel.user_comments),
            selectinload(UserModel.user_stories),
            selectinload(UserModel.liked_posts),
            selectinload(UserModel.liked_stories),
            selectinload(UserModel.liked_comments),
            selectinload(UserModel.followers),
            selectinload(UserModel.followings)
        ).filter(UserModel.username==username)
        async with self.db_session as session:
            try:
                user= await session.execute(query)
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return user.unique().scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def read_by_email(self,email:EmailStr):
        query=sql.select(UserModel).options(
            selectinload(UserModel.user_posts),
            selectinload(UserModel.user_comments),
            selectinload(UserModel.user_stories),
            selectinload(UserModel.liked_posts),
            selectinload(UserModel.liked_stories),
            selectinload(UserModel.liked_comments),
            selectinload(UserModel.followers),
            selectinload(UserModel.followings)
        ).filter(UserModel.email==email)
        async with self.db_session as session:
            try:
                user= await session.execute(query)
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return user.scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def read_for_sign(self,data:UserSigninSchema):
        if '@' in data.username:
            query=sql.select(UserModel).filter(UserModel.email==data.username)
        else:
            query=sql.select(UserModel).filter(UserModel.username==data.username)
        async with self.db_session as session:
            try:
                user= await session.execute(query)
                user_data=user.scalar_one_or_none()
                if not user_data:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                if not verify_password(data.password,str(user_data.password)):
                    raise HTTPException( detail="Invalid Credentials",status_code=status.HTTP_401_UNAUTHORIZED)
                return user_data
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def add(self,user_data:UserAddSchema|UserAddAdminSchema):
        user=UserModel(**user_data.dict())
        user.password = hashed_password(user_data.password)
        user.user_posts=[]
        async with self.db_session as session:
            try:
                session.add(user)
                await session.commit()
                return user
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def change_password(self,user_id:UUID,password_data:UserPasswordChangeSchema):
        query=sql.select(UserModel).filter(UserModel.id==user_id)
        async with self.db_session as session:
            result= await session.execute(query)
            user=result.scalar_one_or_none()
            if not user:
                raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
            if verify_password(password_data.current_password,str(user.password)):
                update_query = sql.update(UserModel).where(UserModel.id==user_id).values(
                    password=password_data.new_password
                )
                await session.execute(update_query)
                await session.commit()
                return {"details":"password changed successfully."}

    async def update(self,user_id:UUID,user_data:UserEditSchema):
        query=sql.select(UserModel).filter(UserModel.id==user_id)
        try:
            async with self.db_session as session:
                result= await session.execute(query)
                user=result.scalar_one_or_none()
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                for key,value in user_data.dict(exclude_unset=True).items():
                    if value is not None:
                        setattr(user,key,value)
                await session.commit()
                return user
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def update_admin(self,user_id:UUID,user_data:UserEditAdminSchema):
        query=sql.select(UserModel).filter(UserModel.id==user_id)
        try:
            async with self.db_session as session:
                result= await session.execute(query)
                user=result.scalar_one_or_none()
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                for key,value in user_data.dict(exclude_unset=True).items():
                    if value is not None:
                        setattr(user,key,value)
                await session.commit()
                return user
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,user_id:UUID):
        query=sql.select(UserModel).filter(UserModel.id==user_id)
        async with self.db_session as session:
            try:
                user=await session.execute(query)
                if not user:
                    raise HTTPException(detail="User Not Found",status_code=status.HTTP_404_NOT_FOUND)
                    await session.delete(user)
                    await session.commit()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
