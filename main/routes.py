from flask import Blueprint, request, jsonify, render_template
from сurrency_service import CurrencyService

currency_bp = Blueprint('currency', __name__)
currency_service = CurrencyService()

@currency_bp.route('/')
def index():
    return render_template('index.html')

@currency_bp.route('/convert', methods=['GET'])
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

    result = currency_service.convert_currency(amount, from_currency, to_currency)
    if result is None:
        return jsonify({"error": "Неверный код валюты."}), 400

    return jsonify({
        "from": from_currency.upper(),
        "to": to_currency.upper(),
        "input": amount,
        "result": result
    })