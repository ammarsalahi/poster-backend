from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,or_
from models import *
from fastapi import HTTPException,status
from uuid import UUID

from typing import List




class UserCrud:

    def __init__(self,db_session:AsyncSession)->None:
        self.db_session=db_session

    async def read_all(self,limit:int,offset:int,is_superuser:bool)->List[UserResponse]:
        if is_superuser:
            query=select(User).offset(offset).limit(limit)
            async with self.db_session as session:
                users = await session.execute(query)
                return users
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
    async def read_one(self,user_id:UUID)->User:
        query=select(User).filter(User.id==user_id)
        async with self.db_session as session:
            user= await session.execute(query)
            if user:
                return user.scalar()
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    async def read_by_username(self,username:str)->User:
        query=select(User).filter(User.username==username)
        async with self.db_session as session:
            user= await session.execute(query)
            if user:
                return user.scalar()
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


    async def add(self,user_data:UserAdd)->UserResponse:
        user=User(**user_data.dict())
        user.password=hashed_password(user_data.password)
        async with self.db_session as session:
            session.add(user)
            await session.commit()
        return user


    async def update(self,user_id:UUID,user_data:UserEdit)->User:
        query=select(User).filter(User.id==user_id)
        try:
            async with self.db_session as session:
                user=session.execute(query)
                if user:
                    for key,value in user_data.dict(exclude_unset=True).items():
                        setattr(user,key,value)
                    await session.commit()
                    return user
                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_308_PERMANENT_REDIRECT,detail=f"Database error {str(e)}")

    async def delete(self,user_id:UUID):
        query=select(User).filter(User.id==user_id)
        async with self.db_session as session:
            user=await session.execute(query)
            if user:
                await session.delete(user)
                await session.commit()
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

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
