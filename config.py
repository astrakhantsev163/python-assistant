import os
from dotenv import load_dotenv
from enum import Enum, StrEnum
from pydantic_settings import BaseSettings

load_dotenv()

RU_DAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


class Settings(BaseSettings):
    API_KEY: str = os.getenv("API_KEY")
    FORECAST_URL: str = "http://api.openweathermap.org/data/2.5/forecast"
    DEFAULT_CITY: str = os.getenv("DEFAULT_CITY")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    USD_TOKEN: str = os.getenv("USD_TOKEN")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASS: str = os.getenv("POSTGRES_PASS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


class Postgres(StrEnum):
    DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASS}@localhost/personal_assistant"


class City(Enum):
    moscow = ("Moscow", "Москва")
    saint_petersburg = ("Saint Petersburg", "Санкт-Петербург")
    novosibirsk = ("Novosibirsk", "Новосибирск")
    yekaterinburg = ("Yekaterinburg", "Екатеринбург")
    kazan = ("Kazan", "Казань")
    nizhny_novgorod = ("Nizhny Novgorod", "Нижний Новгород")
    chelyabinsk = ("Chelyabinsk", "Челябинск")
    samara = ("Samara", "Самара")
    ufa = ("Ufa", "Уфа")
    krasnoyarsk = ("Krasnoyarsk", "Красноярск")
    perm = ("Perm", "Пермь")
    voronezh = ("Voronezh", "Воронеж")
    volgograd = ("Volgograd", "Волгоград")
    krasnodar = ("Krasnodar", "Краснодар")
    saratov = ("Saratov", "Саратов")
    tyumen = ("Tyumen", "Тюмень")
    tolyatti = ("Tolyatti", "Тольятти")
    izhevsk = ("Izhevsk", "Ижевск")
    barnaul = ("Barnaul", "Барнаул")
    ulyanovsk = ("Ulyanovsk", "Ульяновск")
    irkutsk = ("Irkutsk", "Иркутск")
    khabarovsk = ("Khabarovsk", "Хабаровск")
    vladivostok = ("Vladivostok", "Владивосток")
    yaroslavl = ("Yaroslavl", "Ярославль")
    makhachkala = ("Makhachkala", "Махачкала")
    yakutsk = ("Yakutsk", "Якутск")
    simferopol = ("Simferopol", "Симферополь")
    sevastopol = ("Sevastopol", "Севастополь")

    def __init__(self, en_name, ru_name):
        self.en_name = en_name
        self.ru_name = ru_name

    @classmethod
    def choices_ru(cls):
        """Возвращает список городов с русским названием."""
        return [city.value[1] for city in cls]

    @classmethod
    def get_ru_name_by_en(cls, en_name):
        """Получает русское название города по-английски."""
        for city in cls:
            if city.en_name == en_name:
                return city.ru_name
        return None

    @classmethod
    def get_en_name_by_ru(cls, ru_name):
        """Получает английское название города по-русски."""
        for city in cls:
            if city.ru_name == ru_name:
                return city.en_name
        return None


class Translations:
    weather_translations = {
        "Clear": "Ясно",
        "Clouds": "Облачно",
        "Rain": "Дождь",
        "Snow": "Снег",
        "Thunderstorm": "Гроза",
        "Drizzle": "Морось",
        "Mist": "Туман",
        "Smoke": "Дым",
        "Haze": "Мгла",
        "Dust": "Пыль",
        "Fog": "Туман",
        "Sand": "Песок",
        "Ash": "Пепел",
        "Squall": "Шквал",
        "Tornado": "Торнадо"
    }
