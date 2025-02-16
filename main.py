import uvicorn
import logging
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

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


@app.get("/")
async def read_root(request: Request, city_choices: City = settings.DEFAULT_CITY):
    weather = Weather(city_choices)
    date, temperature, humid = weather.get_weather_for_week()
    weather_data = list(zip(date, temperature, humid))
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
async def get_weather_for_week(request: Request, city: str):
    try:
        weather = Weather(city)
        date, temperature, humid = weather.get_weather_for_week()
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "city": city,
                "date": date,
                "temperature": temperature,
                "humid": humid
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "message": f"Ошибка: {str(e)}"}
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, log_level="debug", reload=True)
