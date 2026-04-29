import json
import sys
import os
from typing import List, Dict, Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_loader import get_transactions
from modules.categories import group_by_category, get_top_categories, format_categories
from modules.cashback import get_top_cashback_categories
from modules.card_info import CardInfo


def generate_report(
    transactions: List[Dict[str, Any]],
    card_info: Dict[str, Any],
    top_categories: List[Dict[str, Any]],
    top_cashback: List[Dict[str, Any]],
    currency_rates: List[Dict[str, Any]],
    stock_prices: List[Dict[str, Any]]
) -> Dict[str, Any]:
    expenses = sum(abs(t["amount"]) for t in transactions if t["amount"] < 0)
    incomes = sum(t["amount"] for t in transactions if t["amount"] > 0)
    
    return {
        "card_info": card_info,
        "summary": {
            "total_transactions": len(transactions),
            "total_expenses": round(expenses),
            "total_incomes": round(incomes),
            "balance": round(incomes - expenses)
        },
        "top_categories": top_categories,
        "top_cashback": top_cashback,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
        "transactions": [
            {
                "date": t["date"],
                "amount": abs(t["amount"]),
                "category": t["category"],
                "description": t["description"]
            }
            for t in transactions[:100]
        ]
    }


def save_report_to_json(report: Dict[str, Any], file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    transactions = get_transactions()
    
    card = CardInfo("+7 (900) 123-45-67", "МИР", "Сбербанк")
    
    expenses = group_by_category(transactions)
    top_cats_dict = get_top_categories(expenses)
    top_cats_list = format_categories(top_cats_dict)
    top_cb = get_top_cashback_categories(transactions)
    
    currency_rates = [
        {"currency": "USD", "rate": 92.50},
        {"currency": "EUR", "rate": 100.20}
    ]
    
    stock_prices = [
        {"stock": "SBER", "price": 320.50},
        {"stock": "GAZP", "price": 180.30}
    ]
    
    report = generate_report(
        transactions=transactions,
        card_info=card.get_info(),
        top_categories=top_cats_list,
        top_cashback=top_cb,
        currency_rates=currency_rates,
        stock_prices=stock_prices
    )
    
    save_report_to_json(report, "data/report.json")
    print("✅ Отчёт сохранён в data/report.json")
