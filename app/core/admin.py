
from app.models import UserModel
import sqlalchemy as sql
from app.core.config import settings
from app.core.db import async_session
from fastapi import status ,HTTPException
from app.core.security import hashed_password


user_model=UserModel(
        username=settings.ADMIN_USERNAME,
        email=settings.ADMIN_USERNAME,
        password=hashed_password(f"{settings.ADMIN_PASSWORD}"),
        profile_type="private",
        is_verified=True,
        is_active=True,
        is_superuser=True
    ) 

async def delete_oldadmin():
    query = sql.select(UserModel).filter(UserModel.is_superuser==True)
    async with async_session() as session:
        try:
            result = await session.execute(query)
            user = result.scalars()
            if user:
                await session.delete(user)
                await session.commit()
        except Exception as e:
            raise HTTPException(detail=str(e),status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



async def create_admin_user():
    if settings.IS_OLD_ADMINS_DELETE==True:
        await delete_oldadmin()
    async with async_session() as session:
        try:
            session.add(user_model)
            await session.commit()
        except Exception as e:
            raise HTTPException(
                detail=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


async def init_admin():
    query = sql.select(UserModel).filter(
        sql.and_(
            UserModel.is_superuser==True,
            UserModel.username=="admin"
        )
    )
    async with async_session() as session:
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            await create_admin_user()

