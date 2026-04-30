import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from flask import jsonify, request

from data_loader import get_transactions
from modules.api_client import get_currency_rates, get_stock_prices, load_user_settings
from modules.greet import get_greeting
from modules.services import investment_bank, simple_search, search_by_phone, search_transfers_to_individuals


def filter_transactions_by_date_range(
    transactions: List[Dict[str, Any]], end_date: datetime, period: str
) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по диапазону дат."""
    if period == "W":
        start_date = end_date - timedelta(days=6)
    elif period == "M":
        start_date = end_date.replace(day=1)
    elif period == "Y":
        start_date = end_date.replace(month=1, day=1)
    elif period == "ALL":
        start_date = datetime(1900, 1, 1)
    else:
        start_date = end_date.replace(day=1)

    filtered = []
    for t in transactions:
        try:
            t_date = datetime.strptime(t["date"], "%d.%m.%Y")
            if start_date <= t_date <= end_date:
                filtered.append(t)
        except:
            continue
    return filtered


def group_expenses_by_card(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Группирует расходы по картам."""
    cards = {}
    for t in transactions:
        amount = t.get("amount", 0)
        card = t.get("card_number", "")
        if amount < 0 and card:
            if card not in cards:
                cards[card] = {"total_spent": 0, "cashback": 0}
            cards[card]["total_spent"] += abs(amount)
            cards[card]["cashback"] += t.get("cashback", 0)

    return [
        {
            "last_digits": card[-4:] if len(card) >= 4 else "****",
            "total_spent": round(data["total_spent"], 2),
            "cashback": round(data["cashback"], 2),
        }
        for card, data in cards.items()
    ]


def get_top_transactions(transactions: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
    """Возвращает топ-N транзакций по сумме платежа."""
    sorted_trans = sorted(transactions, key=lambda x: abs(x["amount"]), reverse=True)
    return [
        {
            "date": t["date"],
            "amount": round(abs(t["amount"]), 2),
            "category": t["category"],
            "description": t["description"][:50],
        }
        for t in sorted_trans[:top_n]
    ]


def get_expenses_breakdown(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Анализ расходов."""
    expenses_by_category = {}
    transfers_cash = {}

    for t in transactions:
        amount = t.get("amount", 0)
        if amount < 0:
            category = t.get("category", "Без категории")
            abs_amount = abs(amount)
            expenses_by_category[category] = expenses_by_category.get(category, 0) + abs_amount
            if "Перевод" in category or "Наличные" in category:
                transfers_cash[category] = transfers_cash.get(category, 0) + abs_amount

    total_expenses = round(sum(expenses_by_category.values()))

    sorted_expenses = sorted(expenses_by_category.items(), key=lambda x: x[1], reverse=True)
    main_categories = []
    other_sum = 0

    for i, (cat, amt) in enumerate(sorted_expenses):
        if i < 7:
            main_categories.append({"category": cat, "amount": round(amt)})
        else:
            other_sum += amt

    if other_sum > 0:
        main_categories.append({"category": "Остальное", "amount": round(other_sum)})

    sorted_transfers = sorted(transfers_cash.items(), key=lambda x: x[1], reverse=True)
    transfers_cash_list = [{"category": cat, "amount": round(amt)} for cat, amt in sorted_transfers]

    return {"total": total_expenses, "main": main_categories, "transfers_cash": transfers_cash_list}


def get_income_breakdown(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Анализ поступлений."""
    incomes_by_category = {}
    for t in transactions:
        amount = t.get("amount", 0)
        if amount > 0:
            category = t.get("category", "Без категории")
            incomes_by_category[category] = incomes_by_category.get(category, 0) + amount

    total_incomes = round(sum(incomes_by_category.values()))
    sorted_incomes = sorted(incomes_by_category.items(), key=lambda x: x[1], reverse=True)
    main_categories = [{"category": cat, "amount": round(amt)} for cat, amt in sorted_incomes]

    return {"total": total_incomes, "main": main_categories}


def main_page(date_str: str) -> Dict[str, Any]:
    """Главная страница."""
    try:
        end_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except:
        end_date = datetime.now()

    transactions = get_transactions()
    filtered = filter_transactions_by_date_range(transactions, end_date, "M")

    greeting = get_greeting()
    cards = group_expenses_by_card(filtered)
    top_transactions = get_top_transactions(filtered, 5)

    settings = load_user_settings()
    currency_rates = get_currency_rates(settings.get("user_currencies", []))
    stock_prices = get_stock_prices(settings.get("user_stocks", []))

    return {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }


def events_page(date_str: str, period: str = "M") -> Dict[str, Any]:
    """Страница событий."""
    try:
        end_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except:
        end_date = datetime.now()

    transactions = get_transactions()
    filtered = filter_transactions_by_date_range(transactions, end_date, period)

    expenses = get_expenses_breakdown(filtered)
    incomes = get_income_breakdown(filtered)

    settings = load_user_settings()
    currency_rates = get_currency_rates(settings.get("user_currencies", []))
    stock_prices = get_stock_prices(settings.get("user_stocks", []))

    return {"expenses": expenses, "income": incomes, "currency_rates": currency_rates, "stock_prices": stock_prices}
