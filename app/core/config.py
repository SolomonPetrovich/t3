import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "iDoc App"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str = os.getenv("DATABASE_URL")

    STORAGE_DIR: Path = Path("./storage")
    STORAGE_DIR.mkdir(exist_ok=True)

    OPEANAI_API_KEY: str = os.getenv("OPEANAI_API_KEY", 'some_key')
    OPENAI_MODEL: str = "gpt-5.1-mini"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
