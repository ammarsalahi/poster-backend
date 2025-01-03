from fastapi import FastAPI
from app.api.main import app_router
# from app.core.db import init_db
from app.core import settings
from app.cruds.user import UserCrud
from sqlalchemy.ext.asyncio.session import AsyncSession
# from fastapi.staticfiles import StaticFiles
# from app.core.config import create_folder


app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=settings.DOC_URL,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


# @app.on_event("startup")
# async def init_app():
#     return await UserCrud(AsyncSession).create_admin()
# @app.on_event("startup")
# async def initial_data():
#     return await init_db()

#create media and static folders
# create_folder()

# app.mount("/media", StaticFiles(directory=settings.MEDIA_DIR), name="media")
# app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")


app.include_router(app_router,prefix=settings.API_V1_STR)
