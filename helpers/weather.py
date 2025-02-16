import logging
from functools import lru_cache
from datetime import datetime

import requests

from config import settings, RU_DAYS, Translations, City

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Weather:

    def __init__(self, city):
        self.city = city
        self.forecast_url = f"{settings.FORECAST_URL}?q={city}&appid={settings.API_KEY}&units=metric"

    @lru_cache(maxsize=10)
    def get_weather_for_17_hours(self) -> tuple:
        """
        Получает погоду за 17 часов
        :return: Кортеж с днем недели, временем, температурой, типом погоды
        """
        response = requests.get(f"{self.forecast_url}&cnt=7")
        data = response.json()
        weather = {
            "day_of_week": [],
            "time": [],
            "temperature": [],
            "weather_type": []
        }
        day_of_week_list = weather["day_of_week"]
        time_list = weather["time"]
        temperature_list = weather["temperature"]
        weather_type_list = weather["weather_type"]

        if response.status_code == 200:
            for day in data['list'][:7]:
                date = datetime.strptime(day['dt_txt'], '%Y-%m-%d %H:%M:%S')
                day_of_week = RU_DAYS[date.weekday()]
                time = date.time()
                temperature = int(day['main']['temp'])
                try:
                    weather_type_en = day['weather'][0]['main']
                    weather_type = Translations.weather_translations[weather_type_en]
                except KeyError:
                    weather_type = "Неизвестно"
                day_of_week_list.append(day_of_week)
                time_list.append(time)
                temperature_list.append(temperature)
                weather_type_list.append(weather_type)

            logger.info(f"Получены данные о погоде: \n {weather}")
            return day_of_week_list, time_list, temperature_list, weather_type_list

        if response.status_code != 200:
            raise ValueError(f"Ошибка API: {response.status_code} - {response.text}")

        print("Ошибка при получении данных:", response.status_code)