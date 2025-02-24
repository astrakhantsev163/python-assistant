from datetime import date
from functools import wraps

from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from config import City, logger
from db.cruds import crud_doctors
from db.postgres import get_postgres
from helpers.news import News

templates = Jinja2Templates(directory="templates")


def render_main_template(template_name: str):
    """
    Декоратор для рендеринга шаблонов Главной страницы
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            if not request:
                raise ValueError("Объект Request не был получен")
            data = await func(*args, **kwargs)
            if not isinstance(data, dict):
                raise ValueError(
                    "Функция должна возвращать словарь с данными для контекста."
                )
            usd = "Нет данных"
            eur = "Нет данных"
            try:
                news = News()
                currency_data = news.get_currency_rates(["USD", "EUR"])
                usd = round(float(currency_data["USD"]), 2)
                eur = round(float(currency_data["EUR"]), 2)
            except Exception as e:
                logger.error(f"Ошибка при получении валют. Причина: {e}")
            context = {
                "request": request,
                "today": date.today().strftime("%d.%m.%Y"),
                "usd": usd,
                "eur": eur,
                "city_choices": City.choices_ru(),
                "selected_city": data.get("selected_city"),
            }

            full_context = {**context, **data}
            return templates.TemplateResponse(template_name, full_context)

        return wrapper

    return decorator


def render_doctors(
    template_name: str,
    skip: int = 0,
    limit: int = 25,
):
    """
    Декоратор для рендеринга шаблонов страницы Докторов
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            if not request:
                raise ValueError("Объект Request не был получен")
            doctors_data = await func(*args, **kwargs)
            if not isinstance(doctors_data, dict):
                raise ValueError(
                    "Функция должна возвращать словарь с данными для контекста."
                )
            db: Session = next(get_postgres())
            full_name, specialization, price, address = crud_doctors.get_doctors(
                db, skip=skip, limit=limit
            )
            doctors_data = list(zip(full_name, specialization, price, address))
            context = {
                "request": request,
                "doctors": doctors_data,
            }
            return templates.TemplateResponse(template_name, context)

        return wrapper

    return decorator
