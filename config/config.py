import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME")
    APP_PORT: int = os.getenv("APP_PORT")
    APP_HOST: str = os.getenv("APP_HOST")
    APP_ENV: str = os.getenv("APP_ENV")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB: str = os.getenv("MYSQL_DB")
    MYSQL_HOST: str = os.getenv("MYSQL_HOST")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT")

settings = Settings()