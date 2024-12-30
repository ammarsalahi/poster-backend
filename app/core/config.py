from pydantic_settings import BaseSettings,SettingsConfigDict
import asyncio
import os
from dotenv import load_dotenv
from typing import Optional


load_dotenv()


class Settings(BaseSettings):
    model_config=SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_NAME:str = "Poster"
    DOC_URL:str = "/"
    API_V1_STR:str  = "/api/v1"
    MEDIA_DIR:str = "media"
    STATIC_DIR:str = "static"
    SMTP_HOST:Optional[str] = os.getenv("SMTP_HOST")
    SMTP_USERNAME:Optional[str]  = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD:Optional[str]  = os.getenv("SMTP_PASSWORD")
    SMTP_PORT:Optional[str]  = os.getenv("SMTP_PORT")
    GOOGLE_CLIENT_ID:Optional[str]  = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET:Optional[str]  = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI:Optional[str]  = os.getenv("GOOGLE_REDIRECT_URI")
    ADMIN_USERNAME:Optional[str]  = os.getenv("ADMIN_USERNAME")
    ADMIN_EMAIL:Optional[str]  = os.getenv("ADMIN_EMAIL")
    ADMIN_PASSWORD:Optional[str]  = os.getenv("ADMIN_PASSWORD")
    IS_OLD_ADMINS_DELETE:Optional[str]  = os.getenv("IS_OLD_ADMINS_DELETE")



settings = Settings()



def create_folder():
    os.makedirs(settings.MEDIA_DIR,exist_ok=True)
    os.makedirs(settings.STATIC_DIR,exist_ok=True)
