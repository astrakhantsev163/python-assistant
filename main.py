from datetime import date
from threading import Thread

import uvicorn
import logging
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi import Response

from starlette.staticfiles import StaticFiles

from config import City, settings
from helpers.news import News
from helpers.weather import Weather

from telegram_bot.telegram_bot import TelegramBot

templates_path = Path(__file__).parent / "templates"
styles = Path(__file__).parent / "static"

app = FastAPI()
telegram_bot = TelegramBot()
templates = Jinja2Templates(directory=templates_path.resolve())
app.mount("/static", StaticFiles(directory=styles.resolve()), name="static")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Приложение запущено")


@app.on_event("startup")
async def startup_bot():
    bot_thread = Thread(target=telegram_bot.run_bot, daemon=True)
    bot_thread.start()


@app.on_event("shutdown")
async def shutdown_bot():
    telegram_bot.stop_bot()
    logger.info("Телеграм бот завершил работу")


@app.middleware("http")
async def add_no_cache_headers(request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response


@app.get("/")
async def read_root(
    request: Request,
    city_choices: str = settings.DEFAULT_CITY
):
    selected_city = next((city for city in City if city.ru_name == city_choices))
    weather = Weather(selected_city.en_name)
    day_of_week, time, temperature, weather_type = weather.get_weather_for_17_hours()
    weather_data = list(zip(day_of_week, time, temperature, weather_type))
    news = News()
    usd = "Нет данных"
    eur = "Нет данных"
    try:
        currency_data = news.get_currency_rates(["USD", "EUR"])
        usd = round(float(currency_data["USD"]), 2)
        eur = round(float(currency_data["EUR"]), 2)
    except Exception as e:
        logger.error(f"Ошибка при получении валют. Причина: {e}")
    today = date.today().strftime("%d.%m.%Y")
    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
            "today": today,
            "usd": usd,
            "eur": eur,
            "weather_data": weather_data,
            "city_choices": City.choices_ru(),
            "selected_city": selected_city.ru_name
        },
    )


@app.get("/weather")
async def get_weather_17_hours(request: Request, city: str, response: Response):
    try:
        city_en = City.get_en_name_by_ru(city)
        response.set_cookie(key="selected_city", value=city_en)
        weather = Weather(city_en)
        day_of_week, time, temperature, weather_type = weather.get_weather_for_17_hours()
        weather_data = list(zip(day_of_week, time, temperature, weather_type))
        news = News()
        usd = "Нет данных"
        eur = "Нет данных"
        try:
            currency_data = news.get_currency_rates(["USD", "EUR"])
            usd = round(float(currency_data["USD"]), 2)
            eur = round(float(currency_data["EUR"]), 2)
        except Exception as e:
            logger.error(f"Ошибка при получении валют. Причина: {e}")
        today = date.today().strftime("%d.%m.%Y")
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "today": today,
                "usd": usd,
                "eur": eur,
                "weather_data": weather_data,
                "city_choices": City.choices_ru(),
                "selected_city": city
            }
        )
    except ValueError as e:
        print(f"{e}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, log_level="debug", reload=True)
