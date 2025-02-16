from functools import lru_cache

import requests

from config import settings


class Weather:

    def __init__(self, city: str):
        self.city = city
        self.forecast_url = f"{settings.FORECAST_URL}?q={settings.DEFAULT_CITY}&appid={settings.API_KEY}&units=metric"

    @lru_cache(maxsize=10)
    def get_weather_for_week(self) -> tuple:
        """
        Получает погоду за 7 дней
        :return: Кортеж с датой, температурой, влажностью
        """
        response = requests.get(self.forecast_url)
        data = response.json()
        weather = {
            "date": [],
            "temperature": [],
            "humid": []
        }
        if response.status_code == 200:
            print("Получены данные о погоде:")
            for day in data['list'][:7]:
                date = day['dt_txt']
                temperature = day['main']['temp']
                humid = day['main']['humidity']
                weather.get("date", []).append(date)
                weather.get("temperature", []).append(temperature)
                weather.get("humid", []).append(humid)
            date = weather.get("date", [])
            temperature = weather.get("temperature", [])
            humid = weather.get("humid", [])
            return date, temperature, humid
        if response.status_code != 200:
            raise ValueError(f"Ошибка API: {response.status_code} - {response.text}")
        else:
            print("Ошибка при получении данных:", response.status_code)
