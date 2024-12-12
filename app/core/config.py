from pydantic_settings import BaseSettings,SettingsConfigDict
import asyncio
import os

class Settings(BaseSettings):
    model_config=SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_NAME:str = "Poster"
    DOC_URL:str = "/"
    API_V1_STR:str  = "/api/v1"
    MEDIA_DIR:str="media"
    STATIC_DIR:str="static"
    SMTP_HOST:str = ""
    SMTP_USERNAME:str = ""
    SMTP_PASSWORD:str = ""
    SMTP_PORT:int=0

settings = Settings()



def create_folder():
    os.makedirs(settings.MEDIA_DIR,exist_ok=True)
    os.makedirs(settings.STATIC_DIR,exist_ok=True)
