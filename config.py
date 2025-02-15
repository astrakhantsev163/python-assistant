import os
from dotenv import load_dotenv
from enum import StrEnum

load_dotenv()

API_KEY = os.getenv("API_KEY")

FORECATS_API_URL = f"https://api.openweathermap.org/data/2.5/forecast"


class City(StrEnum):
    moscow = "Moscow"
    saint_petersburg = "Saint petersburg"
