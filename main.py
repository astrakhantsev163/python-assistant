from threading import Thread
import uvicorn
from config import logger
from fastapi import FastAPI, Request, HTTPException, Response
from pathlib import Path
from starlette.staticfiles import StaticFiles
from config import City, settings
from helpers.weather import Weather
from routers import doctors
from telegram_bot.telegram_bot import TelegramBot
from utils.decorators import render_main_template


templates_path = Path(__file__).parent / "templates"
styles = Path(__file__).parent / "static"

app = FastAPI()
telegram_bot = TelegramBot()
app.mount("/static", StaticFiles(directory=styles.resolve()), name="static")

logger.info("Приложение запущено")

app.include_router(doctors.router)


# Middleware для отключения кэширования
@app.middleware("http")
async def add_no_cache_headers(request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response


#  Главная страница
@app.get("/")
@render_main_template("index.html")
async def get_main_page(request: Request, city_choices: str = settings.DEFAULT_CITY):
    try:
        selected_city = next((city for city in City if city.ru_name == city_choices))
        weather = Weather(selected_city.en_name)
        day_of_week, time, temperature, weather_type = weather.get_weather_for_21_hours()
        weather_data = list(zip(day_of_week, time, temperature, weather_type))

        return {
            "weather_data": weather_data,
            "selected_city": selected_city.ru_name,
        }
    except Exception as e:
        logger.error(f"{e}")


@app.get("/weather")
@render_main_template("index.html")
async def get_weather_21_hours(request: Request, city: str, response: Response):
    try:
        city_en = City.get_en_name_by_ru(city)
        response.set_cookie(key="selected_city", value=city_en)
        weather = Weather(city_en)
        day_of_week, time, temperature, weather_type = weather.get_weather_for_21_hours()
        weather_data = list(zip(day_of_week, time, temperature, weather_type))

        return {
            "weather_data": weather_data,
            "selected_city": city,
        }
    except Exception as e:
        logger.error(f"{e}")


# Запуск Telegram-бота
@app.on_event("startup")
async def startup_bot():
    bot_thread = Thread(target=telegram_bot.run_bot, daemon=True)
    bot_thread.start()


@app.on_event("shutdown")
async def shutdown_bot():
    telegram_bot.stop_bot()
    logger.info("Телеграм бот завершил работу")


# Запуск приложения
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)
