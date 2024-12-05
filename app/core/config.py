from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    model_config=SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_NAME:str = "Poster"
    DOC_URL:str = "/"
    API_V1_STR:str  = "/api/v1"

settings = Settings()
