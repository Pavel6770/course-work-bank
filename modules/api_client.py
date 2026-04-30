import requests
import json
from typing import List, Dict, Any


def load_user_settings() -> Dict[str, Any]:
    with open("user_settings.json", "r", encoding="utf-8") as f:
        return json.load(f)


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """Получает текущие курсы валют к RUB."""
    rates = []

    # Моковые данные для демонстрации (если API не работает)
    mock_rates = {"USD": 92.50, "EUR": 100.20, "GBP": 115.30, "CNY": 12.80}

    try:
        # Попробуем получить реальные курсы
        url = "https://api.frankfurter.app/latest?from=RUB"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            for currency in currencies:
                rate = data.get("rates", {}).get(currency, 0)
                rates.append({"currency": currency, "rate": round(rate, 2)})
        else:
            # Используем моковые данные
            for currency in currencies:
                rate = mock_rates.get(currency, 0)
                rates.append({"currency": currency, "rate": rate})
    except Exception as e:
        print(f"Ошибка получения курсов валют: {e}")
        # Используем моковые данные
        for currency in currencies:
            rate = mock_rates.get(currency, 0)
            rates.append({"currency": currency, "rate": rate})

    return rates


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Получает текущие цены акций."""
    prices = []

    # Моковые данные для демонстрации
    mock_prices = {"AAPL": 175.50, "AMZN": 145.30, "GOOGL": 138.20, "MSFT": 420.80, "TSLA": 215.60}

    try:
        import yfinance as yf

        for stock in stocks:
            ticker = yf.Ticker(stock)
            hist = ticker.history(period="1d")
            if not hist.empty:
                price = hist["Close"].iloc[-1]
                prices.append({"stock": stock, "price": round(price, 2)})
            else:
                prices.append({"stock": stock, "price": mock_prices.get(stock, 100.0)})
    except ImportError:
        print("yfinance не установлен. Используем моковые данные")
        for stock in stocks:
            prices.append({"stock": stock, "price": mock_prices.get(stock, 100.0)})
    except Exception as e:
        print(f"Ошибка получения цен акций: {e}")
        for stock in stocks:
            prices.append({"stock": stock, "price": mock_prices.get(stock, 100.0)})

    return prices


if __name__ == "__main__":
    settings = load_user_settings()
    print("Курсы валют:", get_currency_rates(settings["user_currencies"]))
    print("Цены акций:", get_stock_prices(settings["user_stocks"]))
