import uvicorn
import logging
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi import Response

from starlette.staticfiles import StaticFiles

from config import City, settings
from helpers.weather import Weather

templates_path = Path(__file__).parent / "templates"
styles = Path(__file__).parent / "static"

app = FastAPI()
templates = Jinja2Templates(directory=templates_path.resolve())
app.mount("/static", StaticFiles(directory=styles.resolve()), name="static")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Приложение запущено")


@app.middleware("http")
async def add_no_cache_headers(request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response


@app.get("/")
async def read_root(request: Request, city_choices: City = settings.DEFAULT_CITY):
    weather = Weather(city_choices)
    day_of_week, time, temperature, weather_type = weather.get_weather_for_17_hours()
    weather_data = list(zip(day_of_week, time, temperature, weather_type))
    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
            "weather_data": weather_data,
            "city_choices": [e.value for e in City],
            "selected_city": city_choices.value
        },
    )


@app.get("/weather")
async def get_weather_for_week(request: Request, city: str, response: Response):
    try:
        response.set_cookie(key="selected_city", value=city)
        weather = Weather(city)
        day_of_week, time, temperature, weather_type = weather.get_weather_for_17_hours()
        weather_data = list(zip(day_of_week, time, temperature, weather_type))
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "city": city,
                "weather_data": weather_data,
                "city_choices": [e.value for e in City],
                "selected_city": city
            }
        )
    except ValueError as e:
        print(f"{e}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, log_level="debug", reload=True)
