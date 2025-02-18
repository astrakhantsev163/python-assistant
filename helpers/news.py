import requests

from config import settings


class News:
    def __init__(self):
        self.URL_USD = (
            f"https://v6.exchangerate-api.com/v6/{settings.USD_TOKEN}/latest/"
        )

    def get_currency_rates(self, currency: list) -> dict | str:
        rates = {}
        for rate in currency:
            try:
                response = requests.get(f"{self.URL_USD}{rate}")
                data = response.json()
                if data["result"] == "success":
                    rub_currency = data["conversion_rates"]["RUB"]
                    rates[rate] = rub_currency
            except Exception as e:
                return f"Данные о курсе валют не были получены. Причина: {e}"
        return rates


if __name__ == "__main__":
    news = News()
    print(news.get_currency_rates(["USD", "EUR"]))
