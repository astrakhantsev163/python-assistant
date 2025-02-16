import os
from dotenv import load_dotenv
from enum import StrEnum
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    API_KEY: str = os.getenv("API_KEY")
    FORECAST_URL: str = "http://api.openweathermap.org/data/2.5/forecast"
    DEFAULT_CITY: str = os.getenv("DEFAULT_CITY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


class City(StrEnum):
    moscow = "Moscow"
    saint_petersburg = "Saint petersburg"

    @classmethod
    def choices(cls):
        return [e.value for e in cls]
