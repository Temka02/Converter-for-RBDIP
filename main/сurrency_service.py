import requests

class CurrencyService:
    def __init__(self):
        self.exchange_rates = {
            'USD': 1.0,
            'EUR': 0.9,
            'GBP': 0.8,
            'JPY': 110.0,
            'RUB': 75.0
        }
        self.update_rates_from_api()

    def get_rate(self, currency):
        if not currency:
            return None
        return self.exchange_rates.get(currency.upper())

    def convert_currency(self, amount, from_currency, to_currency):
        rate_from = self.get_rate(from_currency)
        rate_to = self.get_rate(to_currency)
        if rate_from is None or rate_to is None:
            return None
        amount_in_usd = amount / rate_from
        return amount_in_usd * rate_to

    def update_rates_from_api(self):
        url = f"https://api.exchangerate.host/live?access_key=1ab04c2868b77cc3b7a080d57cec7da7"
        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                if data.get("success"):
                    quotes = data.get("quotes", {})
                    if quotes:
                        self.exchange_rates.update({
                            k[3:]: float(v) for k, v in quotes.items()
                        })
                        return True
                else:
                    print("Ошибка API:", data.get("error", {}).get("info", "Неизвестная ошибка"))
        except Exception as e:
            print(f"Ошибка при обновлении курсов: {e}")
        return False