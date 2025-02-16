import os
from dotenv import load_dotenv
from enum import StrEnum
from pydantic_settings import BaseSettings

load_dotenv()

RU_DAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]


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
    novosibirsk = "Novosibirsk"
    yekaterinburg = "Yekaterinburg"
    kazan = "Kazan"
    nizhny_novgorod = "Nizhny novgorod"
    chelyabinsk = "Chelyabinsk"
    samara = "Samara"
    ufa = "Ufa"
    krasnoyarsk = "Krasnoyarsk"
    perm = "Perm"
    voronezh = "Voronezh"
    volgograd = "Volgograd"
    krasnodar = "Krasnodar"
    saratov = "Saratov"
    tyumen = "Tyumen"
    tolyatti = "Tolyatti"
    izhevsk = "Izhevsk"
    barnaul = "Barnaul"
    ulyanovsk = "Ulyanovsk"
    irkutsk = "Irkutsk"
    khabarovsk = "Khabarovsk"
    vladivostok = "Vladivostok"
    yaroslavl = "Yaroslavl"
    makhachkala = "Makhachkala"
    yakutsk = "Yakutsk"
    simferopol = "Simferopol"
    sevastopol = "Sevastopol"

    @classmethod
    def choices(cls):
        return [e.value for e in cls]


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
    city_translations = {
        "Moscow": "Москва",
        "Saint Petersburg": "Санкт-Петербург",
        "Novosibirsk": "Новосибирск",
        "Yekaterinburg": "Екатеринбург",
        "Kazan": "Казань",
        "Nizhny Novgorod": "Нижний Новгород",
        "Chelyabinsk": "Челябинск",
        "Samara": "Самара",
        "Ufa": "Уфа",
        "Krasnoyarsk": "Красноярск",
        "Perm": "Пермь",
        "Voronezh": "Воронеж",
        "Volgograd": "Волгоград",
        "Krasnodar": "Краснодар",
        "Saratov": "Саратов",
        "Tyumen": "Тюмень",
        "Tolyatti": "Тольятти",
        "Izhevsk": "Ижевск",
        "Barnaul": "Барнаул",
        "Ulyanovsk": "Ульяновск",
        "Irkutsk": "Иркутск",
        "Khabarovsk": "Хабаровск",
        "Vladivostok": "Владивосток",
        "Yaroslavl": "Ярославль",
        "Makhachkala": "Махачкала",
        "Yakutsk": "Якутск",
        "Simferopol": "Симферополь",
        "Sevastopol": "Севастополь"
    }
