import json
import re
import math
import logging
from datetime import datetime
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# ============================================================
# 1. Выгодные категории повышенного кешбэка
# ============================================================


def calculate_cashback_by_category(transactions: List[Dict[str, Any]], year: int, month: int) -> Dict[str, float]:
    """Анализирует, сколько кешбэка можно заработать по каждой категории."""
    logger.info(f"Расчёт кешбэка за {year}-{month:02d}")

    expenses_by_category = {}

    for t in transactions:
        try:
            t_date = datetime.strptime(t["date"], "%d.%m.%Y")
            amount = t.get("amount", 0)
            if isinstance(amount, str):
                amount = float(amount)

            if t_date.year == year and t_date.month == month and amount < 0:
                category = t.get("category", "Без категории")
                expenses_by_category[category] = expenses_by_category.get(category, 0) + abs(amount)
        except Exception as e:
            continue

    return {cat: round(amt / 100, 2) for cat, amt in expenses_by_category.items()}


# ============================================================
# 2. Инвесткопилка
# ============================================================


def round_up(amount: float, limit: int) -> float:
    """Округляет сумму до ближайшего кратного limit вверх."""
    if amount <= 0:
        return amount
    return math.ceil(amount / limit) * limit


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Рассчитывает сумму, которую удалось бы отложить в Инвесткопилку."""
    logger.info(f"Расчёт инвесткопилки за {month} с шагом {limit}")

    total_saved = 0.0

    for t in transactions:
        date_str = t.get("date", "")
        amount_raw = t.get("amount", 0)

        # Преобразуем amount в число
        try:
            amount = float(amount_raw)
        except (ValueError, TypeError):
            continue

        # Только расходы
        if amount >= 0:
            continue

        # Проверяем месяц
        try:
            t_date = datetime.strptime(date_str, "%d.%m.%Y")
            t_month = t_date.strftime("%Y-%m")
        except Exception:
            continue

        if t_month != month:
            continue

        # Округляем сумму
        abs_amount = abs(amount)
        rounded = round_up(abs_amount, limit)
        saved = rounded - abs_amount
        total_saved += saved
        logger.debug(f"Сумма: {abs_amount}, округлено: {rounded}, отложено: {saved}")

    logger.info(f"За месяц накоплено: {total_saved:.2f} руб.")
    return round(total_saved, 2)


# ============================================================
# 3. Простой поиск
# ============================================================


def simple_search(transactions: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """Ищет транзакции по подстроке в описании или категории."""
    logger.info(f"Поиск: '{query}'")
    q_lower = query.lower()
    return [
        t
        for t in transactions
        if q_lower in t.get("description", "").lower() or q_lower in t.get("category", "").lower()
    ]


# ============================================================
# 4. Поиск по телефонным номерам
# ============================================================

PHONE_PATTERN = re.compile(r'(\+7|8)?[\s\-]?\(?(\d{3})\)?[\s\-]?(\d{3})[\s\-]?(\d{2})[\s\-]?(\d{2})')


def contains_phone_number(text: str) -> bool:
    """Проверяет, содержит ли текст телефонный номер."""
    return bool(PHONE_PATTERN.search(text))


def search_by_phone(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Возвращает транзакции, содержащие в описании телефонные номера."""
    logger.info("Поиск транзакций с телефонными номерами")
    return [t for t in transactions if contains_phone_number(t.get("description", ""))]


# ============================================================
# 5. Поиск переводов физическим лицам
# ============================================================

NAME_PATTERN = re.compile(r'([А-ЯЁ][а-яё]+)\s+([А-ЯЁ]\.?)')


def is_transfer_to_person(transaction: Dict[str, Any]) -> bool:
    """Проверяет, является ли транзакция переводом физическому лицу."""
    if transaction.get("category") != "Переводы":
        return False
    return bool(NAME_PATTERN.search(transaction.get("description", "")))


def search_transfers_to_individuals(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Возвращает транзакции, относящиеся к переводам физическим лицам."""
    logger.info("Поиск переводов физическим лицам")
    return [t for t in transactions if is_transfer_to_person(t)]


if __name__ == "__main__":
    from data_loader import get_transactions

    transactions = get_transactions()

    print("\n" + "=" * 60)
    print("1. Выгодные категории кешбэка за декабрь 2021:")
    cashback = calculate_cashback_by_category(transactions, 2021, 12)
    for cat, amt in list(cashback.items())[:10]:
        print(f"   {cat}: {amt:.2f} руб.")

    print("\n" + "=" * 60)
    print("2. Инвесткопилка за декабрь 2021 (шаг 50 руб.):")
    saved = investment_bank("2021-12", transactions, 50)
    print(f"   Накоплено: {saved:.2f} руб.")
