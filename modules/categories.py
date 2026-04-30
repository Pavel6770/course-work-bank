from typing import List, Dict, Any
from collections import defaultdict


def group_by_category(transactions: List[Dict[str, Any]]) -> Dict[str, float]:
    """Группирует расходы по категориям (только бизнес-логика)."""
    expenses = defaultdict(float)
    for t in transactions:
        amount = t.get('amount', 0)
        if amount < 0:
            expenses[t.get('category', 'Без категории')] += abs(amount)
    return dict(expenses)


def get_top_categories(expenses: Dict[str, float], top_n: int = 7) -> Dict[str, float]:
    """Возвращает топ-N категорий + Остальное."""
    sorted_expenses = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
    top = dict(sorted_expenses[:top_n])
    other_sum = sum(amount for _, amount in sorted_expenses[top_n:])
    if other_sum > 0:
        top["Остальное"] = round(other_sum)
    return top


def format_categories(categories: Dict[str, float]) -> List[Dict[str, Any]]:
    """Форматирует категории для JSON."""
    return [{"category": cat, "amount": int(round(amount))} for cat, amount in categories.items()]


if __name__ == "__main__":
    from data_loader import get_test_transactions

    test_data = get_test_transactions()
    expenses = group_by_category(test_data)
    top = get_top_categories(expenses)
    print("Топ категорий (тест):")
    for cat, amount in top.items():
        print(f"   {cat}: {amount:.0f} руб.")
