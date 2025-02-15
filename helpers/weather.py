import requests

from config import API_KEY, FORECATS_API_URL

CITY = "Saint petersburg"


class Weather:

    def __init__(self):
        self.forecast_url = f"{FORECATS_API_URL}?q={CITY}&appid={API_KEY}&units=metric"

    def get_weather_for_week(self):
        """
        Получает погоду за 7 дней
        :return:
        """
        response = requests.get(self.forecast_url)
        data = response.json()
        if response.status_code == 200:
            print("Получены данные о погоде:")
            for day in data['list'][:7]:
                date = day['dt_txt']
                temp = day['main']['temp']
                humidity = day['main']['humidity']
                print(f"Дата: {date}, Температура: {temp}°C, Влажность: {humidity}%")
        else:
            print("Ошибка при получении данных:", response.status_code)
