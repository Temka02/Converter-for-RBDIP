import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main.сurrency_service import CurrencyService

@pytest.fixture
def service():
    return CurrencyService()

def test_conversion(service):
    result = service.convert_currency(100, "USD", "EUR")
    assert result is not None
    assert result > 0

def test_invalid_currency(service):
    result = service.convert_currency(100, "XXX", "EUR")
    assert result is None

def test_case_insensitivity(service):
    result_lower = service.convert_currency(100, "usd", "eur")
    result_mixed = service.convert_currency(100, "UsD", "EuR")
    assert result_lower is not None and result_lower > 0
    assert result_mixed == result_lower

def test_same_currency_conversion(service):
    result = service.convert_currency(100, "USD", "USD")
    assert result == 100

def test_zero_amount_conversion(service):
    result = service.convert_currency(0, "USD", "EUR")
    assert result == 0

def test_negative_amount_conversion(service):
    result = service.convert_currency(-100, "USD", "EUR")
    assert result is not None
    assert result < 0

def test_invalid_amount_type(service):
    with pytest.raises(TypeError):
        service.convert_currency("сто", "USD", "EUR")

def test_update_rates_from_api(service):
    success = service.update_rates_from_api()
    assert success is True
    assert "EUR" in service.exchange_rates  # Проверяем, что курс евро обновился

def test_conversion_with_missing_currency(service):
    """ Проверка обработки отсутствующего кода валюты """
    result = service.convert_currency(100, None, "EUR")
    assert result is None