import requests
import json
from Fiat_bot.config import values


# get_data("https://cash.rbc.ru/cash/converter.html?from=RUR&to=USD&sum=200&date=&rate=cbrf")

class ConvertionException(Exception):
    pass


class FiatConverter:
    @staticmethod
    def convert(base: str, quote: str, amount: str):
        if quote == base:
            raise ConvertionException(f"Невозможно перевести одинаковые валюты {base}")

        if base not in values:
            raise ConvertionException(f"Валюты {base} нет в списке")

        if quote not in values:
            raise ConvertionException(f"Валюты {quote} нет в списках")

        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        }

        url = f"https://cash.rbc.ru/cash/json/converter_currency_rate/?currency_from={base}&currency_to={quote}&source=cbrf&sum={amount}&date="
        req = requests.get(url, headers)
        total_base = json.loads(req.content)
        result = total_base['data']["sum_result"]
        return result
