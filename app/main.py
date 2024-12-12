from fastapi import FastAPI
from api import app_router
from core.db import init_db
from core import settings
from fastapi.staticfiles import StaticFiles
from core.config import create_folder


app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=settings.DOC_URL,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


# @app.on_event("startup")
# async def initial_data():
#     return await init_db()

#create media and static folders
create_folder()

app.mount("/media", StaticFiles(directory=settings.MEDIA_DIR), name="media")
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")


app.include_router(app_router,prefix=settings.API_V1_STR)
