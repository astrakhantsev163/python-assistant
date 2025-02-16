import requests

from config import API_KEY, FORECATS_API_URL


class Weather:

    def __init__(self, city: str):
        self.city = city
        self.forecast_url = f"{FORECATS_API_URL}?q={self.city}&appid={API_KEY}&units=metric"

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
        else:
            print("Ошибка при получении данных:", response.status_code)
