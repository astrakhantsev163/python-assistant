import logging
from functools import lru_cache

import requests

from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Weather:

    def __init__(self, city: str):
        self.city = city
        self.forecast_url = f"{settings.FORECAST_URL}?q={city}&appid={settings.API_KEY}&units=metric"

    @lru_cache(maxsize=10)
    def get_weather_for_week(self) -> tuple:
        """
        Получает погоду за 7 дней
        :return: Кортеж с датой, температурой, влажностью
        """
        response = requests.get(f"{self.forecast_url}&cnt=7")
        data = response.json()
        weather = {
            "date": [],
            "temperature": [],
            "humid": []
        }
        if response.status_code == 200:
            for day in data['list'][:7]:
                date = day['dt_txt']
                temperature = int(day['main']['temp'])
                humid = day['main']['humidity']
                weather.get("date", []).append(date)
                weather.get("temperature", []).append(temperature)
                weather.get("humid", []).append(humid)
            date = weather.get("date", [])
            temperature = weather.get("temperature", [])
            humid = weather.get("humid", [])
            logger.info(f"Получены данные о погоде: \n {weather}")
            return date, temperature, humid
        if response.status_code != 200:
            raise ValueError(f"Ошибка API: {response.status_code} - {response.text}")
        else:
            print("Ошибка при получении данных:", response.status_code)
