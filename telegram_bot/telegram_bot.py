import logging

import telebot
from telebot.types import ReplyKeyboardRemove

from config import City, settings
from helpers.news import News
from helpers.weather import Weather


class TelegramBot:
    def __init__(self):
        self.bot = telebot.TeleBot(settings.BOT_TOKEN)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Телеграм бот запущен")
        self.register_handlers()
        self.news = News()

    @staticmethod
    def create_main_markup():
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton("Показать погоду"))
        markup.add(telebot.types.KeyboardButton("Получить новости"))
        return markup

    @staticmethod
    def create_city_markup():
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        city_buttons = [
            telebot.types.KeyboardButton(city) for city in City.choices_ru()
        ]
        markup.add(*city_buttons)
        return markup

    @staticmethod
    def create_back_to_main_markup():
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton("Главная страница"))
        return markup

    def register_handlers(self):
        @self.bot.message_handler(commands=["start"])
        def send_welcome(message):
            user_name = message.from_user.first_name
            self.logger.info(f"Боту дали команду /start - {user_name}")
            markup = self.create_main_markup()
            welcome_message = (
                f"Привет, {user_name}! Я — ваш личный ассистент!\n\n"
                "Я буду вам помогать в ваших делах!\n"
                "Ниже можете выбрать чем я могу вам помочь!\n\n"
                "Можно мной полюбоваться тут: https://python-assistant.onrender.com/"
            )
            self.bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

        @self.bot.message_handler(
            func=lambda message: message.text == "Показать погоду"
        )
        def choose_city(message):
            self.logger.info("Бота попросили показать погоду")
            markup = self.create_city_markup()
            self.bot.send_message(
                message.chat.id, "Выберите город из списка:", reply_markup=markup
            )

        @self.bot.message_handler(
            func=lambda message: message.text in City.choices_ru()
        )
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
                        f"Время: {time}\nТемпература: {temperature}°C\nПогода: {weather_type}\n"
                        for _, time, temperature, weather_type in weather_data[:2]
                    ]
                )
                self.bot.send_message(message.chat.id, message_with_weather)
                self.logger.info(f"Бот отправил прогноз погоды. {city}")
            except Exception as e:
                self.bot.send_message(
                    message.chat.id,
                    "Не удалось получить данные о погоде. Попробуйте позже.",
                )
                self.logger.error(f"Бот не смог отправить погоду: {e}")
            finally:
                markup = self.create_back_to_main_markup()
                message_next = (
                    "Можно посмотреть погоду в другом городе или вернуться назад"
                )
                self.bot.send_message(
                    message.chat.id, message_next, reply_markup=markup
                )

        @self.bot.message_handler(
            func=lambda message: message.text == "Главная страница"
        )
        def back_to_main(message):
            self.logger.info("Бота попросили вернуться на главную")
            send_welcome(message)

        # @self.bot.message_handler(func=lambda message: message.text == "Получить новости")
        # def get_time_for_send_news(message):
        #     self.logger.info("Бота попросили запланировать отправку утренних новостей")
        #     markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        #     times = ["8:00", "8:30", "9:00", "9:30", "10:00", "10:30"]
        #     for time in times:
        #         markup.add(telebot.types.KeyboardButton(time))
        #     self.bot.send_message(message.chat.id, "Выберите удобное для вас время", reply_markup=markup)

        @self.bot.message_handler(
            func=lambda message: message.text == "Получить новости"
        )
        def send_news(message):
            user_name = message.from_user.first_name
            self.logger.info(f"У бота запросили новости - {user_name}")
            exchange_rate = self.news.get_currency_rates(["USD", "EUR"])
            message_with_news = (
                f"Курс доллара -> {round(float(exchange_rate['USD']), 2)} рублей.\n"
                f"Курс евро -> {round(float(exchange_rate['EUR']), 2)} рублей.\n"
            )
            markup = self.create_back_to_main_markup()
            self.bot.send_message(
                message.chat.id, message_with_news, reply_markup=markup
            )

        @self.bot.message_handler(commands=["stop"])
        def send_bye_message(message):
            user_name = message.from_user.first_name
            self.logger.info(f"Боту дали команду /stop - {user_name}")
            welcome_message = (
                f"{user_name}, надеюсь я был вам полезен!\n"
                "Если я вам снова понадоблюсь, то отправьте мне команду: /start\n\n"
                "До свидания!"
            )
            self.bot.send_message(
                message.chat.id, welcome_message, reply_markup=ReplyKeyboardRemove()
            )

    def run_bot(self):
        self.bot.polling(none_stop=True)

    def stop_bot(self):
        self.bot.stop_bot()
