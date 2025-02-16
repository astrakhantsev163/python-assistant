from config import Translations


def check_city():
    city = "Москва"
    if city in Translations.city_translations.values():
        for city_en in Translations.city_translations.items():
            if city_en[1] == city:
                city = city_en[0]
                print(city)


if __name__ == "__main__":
    check_city()
