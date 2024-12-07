from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,or_
from models import *
from fastapi import HTTPException,status
from uuid import UUID
from core import hashed_password,verify_password
from typing import List
from pydantic import EmailStr

class UserCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int,is_superuser:bool)->List[UserResponse]:
        if is_superuser:
            query=select(User).offset(offset).limit(limit)
            async with self.db_session as session:
                try:
                    users = await session.execute(query)
                    return users.scalars()
                except Exception as e:
                    raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    async def filter(self,limit:int,offset:int,query:str):
        pass
        # query=select(User).filter(
        #     or_(
        #         User.fullname.
        #     )
        # )
        # query=sql.select(UserModel).filter(
        #     sql.or_(
        #         UserModel.username.ilike(f"%{query}"),
        #         UserModel.fullname.ilike(f"%{query}")
        #     )
        # ).limit(limit).offset(offset)
        # async with self.db_session as session:
        #     users=await session.execute(query)
        #     return users.scalars()
    async def read_one(self,user_id:UUID)->UserResponse:
        query=select(User).filter(User.id==user_id)
        async with self.db_session as session:
            try:
                user= await session.execute(query)
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return user.scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def read_by_username(self,username:str)->UserResponse:
        query=select(User).filter(User.username==username)
        async with self.db_session as session:
            try:
                user= await session.execute(query)
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return user.scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def read_by_email(self,email:EmailStr)->UserResponse:
        query=select(User).filter(User.email==email)
        async with self.db_session as session:
            try:
                user= await session.execute(query)
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                return user.scalar_one()
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def read_for_sign(self,data:UserSignin) -> UserResponse:
        if '@' in data:
            query=select(User).filter(User.email==data.username)
        else:
            query=select(User).filter(User.username==data.username)
        async with self.db_session as session:
            try:
                user= await session.execute(query)
                user_data=user.scalar_one_or_none()
                if not user_data:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                if not verify_password(data.password,user_data.password):
                    raise HTTPException( detail="Invalid Credentials",status_code=status.HTTP_401_UNAUTHORIZED)
                return user_data
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)





    async def add(self,user_data:UserAdd)->UserResponse:
        user=User(**user_data.dict())
        user.password=hashed_password(user_data.password)
        async with self.db_session as session:
            try:
                session.add(user)
                await session.commit()
                return UserResponse(**user.dict())
            except Exception as e:
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def change_password(self,user_id:UUID,password_data:UserPasswordChange):
        query=select(User).filter(User.id==user_id)
        async with self.db_session as session:
            user = await session.execute(query)
            if not user:
                raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
            newuser=User(**user.scalar_one())
            if verify_password(password_data.current_password,newuser.password):
                setattr(user,"password",password_data.new_password)

    async def update(self,user_id:UUID,user_data:UserEdit)->UserResponse:
        query=select(User).filter(User.id==user_id)
        try:
            async with self.db_session as session:
                user= await session.execute(query)
                if not user:
                    raise HTTPException(detail="User Not Found!",status_code=status.HTTP_404_NOT_FOUND)
                for key,value in user_data.dict(exclude_unset=True).items():
                    setattr(user,key,value)
                await session.commit()
                return user.scalar_one()
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,user_id:UUID):
        query=select(User).filter(User.id==user_id)
        async with self.db_session as session:
            try:
                user=await session.execute(query)
                if not user:
                    raise HTTPException(detail="User Not Found",status_code=status.HTTP_404_NOT_FOUND)
                    await session.delete(user)
                    await session.commit()
            except Exception as e
                raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # if is_superuser:
        #     query=sql.select(UserModel).offset(offset).limit(limit)
        #     async with self.db_session as session:
        #         users= await session.execute(query)
        #         return users.scalars()
        # else:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)




    # async def read_one(self,user_id:UUID):
    #     query=sql.select(UserModel).filter(UserModel.id==id)
    #     async with self.db_session as session:
    #         user=await session.execute(query)
    #         if user:
    #             return user.scalar()
    #         else:
    #             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # async def read_by_username(self,username:str):
    #     query=sql.select(UserModel).filter(UserModel.username==username)
    #     async with self.db_session as session:
    #         user=await session.execute(query)
    #         return user.scalar()

    # async def add(self,user_data:UserCreateSchema):
    #     user=UserModel(**user_data.dict())
    #     user.password=hashed_password(user_data.password)
    #     async with self.db_session as session:
    #         session.add(user)
    #         await session.commit()
    #     return user


    # async def update(self,user_id:UUID,user_data:UserUpdateSchema):
    #     query=sql.select(UserModel).filter(UserModel.id==user_id)
    #     try:
    #         async with self.db_session as session:
    #             user=session.execute(session)
    #             if user:
    #                 for key , value in user_data.dict(exclude_unset=True).items():
    #                     setattr(user,key,value)
    #                 await session.commit()
    #                 return user
    #             else:
    #                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    #     except Exception as e:
    #         await session.rollback()
    #         raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    # async def change_password(self,user_id:UUID,password:str):
    #     query=sql.select(UserModel).filter(UserModel.id==user_id)
    #     async with self.db_session as session:
    #         user=await session.execute(query)
    #         if user:
    #             setattr(user,"password",hashed_password(password))
    #             await session.commit()
    #             return user
    #         else:
    #             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
