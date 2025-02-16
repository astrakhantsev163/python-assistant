import logging

import telebot

from config import City, settings
from helpers.weather import Weather

bot = telebot.TeleBot(settings.BOT_TOKEN)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Телеграм бот запущен")


# Обработчик команды /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    logger.info("Боту дали команду /start")
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("Показать погоду"))
    welcome_message = (
        "Привет! Я — ваш личный ассистент!\n\n"
        "Я буду вам помогать в ваших делах!\n"
        "Пока что я только умею показывать вам ближайшую погоду, но в будущем я буду много чего уметь :)\n\n"
        "Ниже, у меня есть кнопка, по которой я покажу вам погоду - тыкайте, не стесняйтесь.\n\n"
        "Можно мной полюбоваться тут: https://python-assistant.onrender.com/"
    )
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)


# Обработчик нажатия кнопки "Показать погоду"
@bot.message_handler(func=lambda message: message.text == "Показать погоду")
def choose_city(message):
    logger.info("Бота попросили показать погоду")
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    city_buttons = [telebot.types.KeyboardButton(city) for city in City.choices_ru()]
    markup.add(*city_buttons)
    bot.send_message(message.chat.id, "Выберите город из списка:", reply_markup=markup)


# Обработчик выбора города
@bot.message_handler(func=lambda message: [message.text for e in City.choices_ru()])
def get_weather(message):
    city = message.text.strip()
    try:
        city_en = City.get_en_name_by_ru(city)
        weather = Weather(city_en)
        (
            day_of_week,
            time,
            temperature,
            weather_type,
        ) = weather.get_weather_for_17_hours()
        weather_data = list(zip(day_of_week, time, temperature, weather_type))
        message_with_weather = "\n".join(
            [
                f"Время: {t}\nТемпература: {temp}°C\nПогода: {w_type}\n"
                for _, t, temp, w_type in weather_data
            ]
        )
        bot.send_message(message.chat.id, message_with_weather)
        logger.info(f"Бот отправил прогноз погоды. {city}")
    except Exception:
        bot.send_message(
            message.chat.id, "Не удалось получить данные о погоде. Попробуйте позже."
        )
        logger.error(f"Бот не смог отправить погоду: {Exception}")
    finally:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton("Показать погоду"))
        message_next = "Можно посмотреть погоду в другом городе:"
        bot.send_message(message.chat.id, message_next, reply_markup=markup)


# Функция для запуска бота
def run_bot():
    bot.polling(none_stop=True)
