from typing import List, Dict, Any
from collections import defaultdict


def get_cashback_by_category(transactions: List[Dict[str, Any]]) -> Dict[str, float]:
    """Суммирует кешбэк по категориям (бизнес-логика)."""
    cashback_by_cat = defaultdict(float)
    for t in transactions:
        amount = t.get('amount', 0)
        cashback = t.get('cashback', 0)
        category = t.get('category', 'Без категории')
        if amount < 0 and cashback > 0:
            cashback_by_cat[category] += cashback
    return dict(cashback_by_cat)


def get_top_cashback_categories(transactions: List[Dict[str, Any]], top_n: int = 3) -> List[Dict[str, Any]]:
    """Возвращает топ-N категорий по кешбэку."""
    cashback_by_cat = get_cashback_by_category(transactions)
    sorted_cb = sorted(cashback_by_cat.items(), key=lambda x: x[1], reverse=True)
    return [{"category": cat, "cashback": int(round(cb))} for cat, cb in sorted_cb[:top_n]]


if __name__ == "__main__":
    from data_loader import get_test_transactions

    test_data = get_test_transactions()
    top_cb = get_top_cashback_categories(test_data)
    print("Топ кешбэк (тест):")
    for item in top_cb:
        print(f"   {item['category']}: {item['cashback']} руб.")
