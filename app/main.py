from fastapi import FastAPI
from api import app_router
from core import settings
app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=settings.DOC_URL,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(app_router,prefix=settings.API_V1_STR)
