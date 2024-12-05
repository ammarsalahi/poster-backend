from fastapi import FastAPI
from api import app_router
app = FastAPI(
    title="Poster API",
    description="v0.0.1",
    docs_url="/"
)

app.include_router(app_router)
