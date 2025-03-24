from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

exchange_rates = {
    'USD': 1.0,
    'EUR': 0.9,
    'GBP': 0.8,
    'JPY': 110.0,
    'RUB': 75.0
}

def get_rate(currency):
    return exchange_rates.get(currency.upper())

def convert_currency(amount, from_currency, to_currency):
    rate_from = get_rate(from_currency)
    rate_to = get_rate(to_currency)
    if rate_from is None or rate_to is None:
        return None
    amount_in_usd = amount / rate_from
    result = amount_in_usd * rate_to
    return result

def update_rates_from_api():
    url = "https://api.exchangerate.host/latest?base=USD"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "rates" in data:
                for key, value in data["rates"].items():
                    exchange_rates[key.upper()] = float(value)
                return True
    except Exception as e:
        print(f"Ошибка при обновлении курсов: {e}")
    return False

@app.route('/convert', methods=['GET'])
def convert():
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    amount = request.args.get('amount')

    if not all([from_currency, to_currency, amount]):
        return jsonify({"error": "Параметры 'from', 'to' и 'amount' обязательны."}), 400

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "'amount' должен быть числом."}), 400

    result = convert_currency(amount, from_currency, to_currency)
    if result is None:
        return jsonify({"error": "Неверный код валюты. Проверьте 'from' и 'to'."}), 400

    return jsonify({
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "input": amount,
        "result": result
    })

@app.route('/rate', methods=['GET'])
def rate():
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')

    if not from_currency or not to_currency:
        return jsonify({"error": "Параметры 'from' и 'to' обязательны."}), 400

    rate_from = get_rate(from_currency)
    rate_to = get_rate(to_currency)
    if rate_from is None or rate_to is None:
        return jsonify({"error": "Неверный код валюты."}), 400

    conversion_rate = rate_to / rate_from
    return jsonify({
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "rate": conversion_rate
    })

@app.route('/currencies', methods=['GET'])
def currencies():
    return jsonify({"currencies": list(exchange_rates.keys())})

@app.route('/update_rates', methods=['POST'])
def update_rates():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Нет данных для обновления."}), 400

    errors = {}
    for key, value in data.items():
        try:
            exchange_rates[key.upper()] = float(value)
        except (ValueError, TypeError):
            errors[key] = "Неверный формат. Значение должно быть числом."

    if errors:
        return jsonify({"error": "Ошибки при обновлении курсов.", "details": errors}), 400

    return jsonify({"message": "Курсы обновлены.", "rates": exchange_rates})

@app.route('/refresh_rates', methods=['GET'])
def refresh_rates():
    if update_rates_from_api():
        return jsonify({"message": "Курсы успешно обновлены из внешнего API.", "rates": exchange_rates})
    else:
        return jsonify({"error": "Не удалось обновить курсы из внешнего API."}), 500

@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Валютный конвертер</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                color: #333;
                margin: 0;
                padding: 20px;
            }
            h1 {
                color: #4CAF50;
            }
            ul {
                list-style: none;
                padding: 0;
            }
            li {
                background: #fff;
                margin: 10px 0;
                padding: 15px;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            code {
                background: #eee;
                padding: 2px 4px;
                border-radius: 3px;
            }
            .container {
                max-width: 800px;
                margin: auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Валютный конвертер</h1>
            <ul>
                <li>Конвертация: <code>/convert?from=USD&amp;to=EUR&amp;amount=100</code></li>
                <li>Получение курса конвертации: <code>/rate?from=USD&amp;to=EUR</code></li>
                <li>Список валют: <code>/currencies</code></li>
                <li>Обновление курсов вручную: <code>/update_rates</code> (POST запрос с JSON данными)</li>
                <li>Обновление курсов из API: <code>/refresh_rates</code></li>
            </ul>
        </div>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    app.run(debug=True)