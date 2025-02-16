import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

from starlette.staticfiles import StaticFiles

from config import City
from helpers.weather import Weather

templates_path = Path(__file__).parent / "templates"
styles = Path(__file__).parent / "static"
# Подключение папки с шаблонами
templates = Jinja2Templates(directory=f"{templates_path}")

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=f"{styles}"),
    name="static",
)


@app.get("/")
async def read_root(request: Request, city_choices: City = City.saint_petersburg):
    weather = Weather(city_choices)
    date, temperature, humid = weather.get_weather_for_week()
    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
            "date": date,
            "temperature": temperature,
            "humid": humid,
            "city_choices": [e.value for e in City],
            "selected_city": city_choices.value
        },
    )


@app.get("/weather")
async def get_weather_for_week(request: Request, city: str):
    weather = Weather(city)
    date, temperature, humid = weather.get_weather_for_week()
    # Передача данных в шаблон
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, log_level="debug", reload=True)
