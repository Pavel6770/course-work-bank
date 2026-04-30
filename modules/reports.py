import sys
import os

# Добавляем путь к корневой папке проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Callable, Any
from functools import wraps
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# ============================================================
# Декоратор для сохранения отчётов в файл
# ============================================================


def save_report(filename: Optional[str] = None):
    """
    Декоратор для сохранения результата функции отчёта в JSON-файл.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"{func.__name__}_{timestamp}.json"
            else:
                output_filename = filename

            try:
                if isinstance(result, pd.DataFrame):
                    data_to_save = result.to_dict(orient="records")
                elif isinstance(result, dict):
                    data_to_save = result
                else:
                    data_to_save = {"result": result}

                with open(output_filename, "w", encoding="utf-8") as f:
                    json.dump(data_to_save, f, ensure_ascii=False, indent=2, default=str)

                logger.info(f"Отчёт сохранён в файл: {output_filename}")
            except Exception as e:
                logger.error(f"Ошибка сохранения отчёта: {e}")

            return result

        return wrapper

    return decorator


# ============================================================
# 1. Траты по категории
# ============================================================


@save_report()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние 3 месяца."""
    if date is None:
        end_date = datetime.now()
    else:
        try:
            end_date = datetime.strptime(date, "%d.%m.%Y")
        except ValueError:
            end_date = datetime.now()

    start_date = end_date - timedelta(days=90)

    logger.info(
        f"Анализ трат по категории '{category}' за период {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}"
    )

    filtered = transactions[
        (transactions["category"] == category)
        & (transactions["amount"] < 0)
        & (pd.to_datetime(transactions["date"], format="%d.%m.%Y") >= start_date)
        & (pd.to_datetime(transactions["date"], format="%d.%m.%Y") <= end_date)
    ]

    filtered = filtered.copy()
    filtered["month"] = pd.to_datetime(filtered["date"], format="%d.%m.%Y").dt.strftime("%Y-%m")
    result = filtered.groupby("month")["amount"].sum().abs().reset_index()
    result.columns = ["month", "total_spent"]

    logger.info(f"Найдено трат: {result['total_spent'].sum():.2f} руб.")
    return result


# ============================================================
# 2. Траты по дням недели
# ============================================================


@save_report()
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает средние траты в каждый день недели за последние 3 месяца."""
    if date is None:
        end_date = datetime.now()
    else:
        try:
            end_date = datetime.strptime(date, "%d.%m.%Y")
        except ValueError:
            end_date = datetime.now()

    start_date = end_date - timedelta(days=90)

    logger.info(
        f"Анализ средних трат по дням недели за период {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}"
    )

    filtered = transactions[
        (transactions["amount"] < 0)
        & (pd.to_datetime(transactions["date"], format="%d.%m.%Y") >= start_date)
        & (pd.to_datetime(transactions["date"], format="%d.%m.%Y") <= end_date)
    ].copy()

    filtered["weekday"] = pd.to_datetime(filtered["date"], format="%d.%m.%Y").dt.day_name(locale="ru")

    result = filtered.groupby("weekday")["amount"].mean().abs().reset_index()
    result.columns = ["weekday", "avg_spent"]

    weekday_order = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    result["order"] = result["weekday"].apply(lambda x: weekday_order.index(x) if x in weekday_order else 7)
    result = result.sort_values("order").drop("order", axis=1)

    logger.info(f"Найдено дней: {len(result)}")
    return result


# ============================================================
# 3. Траты в рабочий/выходной день
# ============================================================


@save_report()
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> dict:
    """Возвращает средние траты в рабочий и выходной день за последние 3 месяца."""
    if date is None:
        end_date = datetime.now()
    else:
        try:
            end_date = datetime.strptime(date, "%d.%m.%Y")
        except ValueError:
            end_date = datetime.now()

    start_date = end_date - timedelta(days=90)

    logger.info(
        f"Анализ трат в рабочие/выходные дни за период {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}"
    )

    filtered = transactions[
        (transactions["amount"] < 0)
        & (pd.to_datetime(transactions["date"], format="%d.%m.%Y") >= start_date)
        & (pd.to_datetime(transactions["date"], format="%d.%m.%Y") <= end_date)
    ].copy()

    filtered["weekday"] = pd.to_datetime(filtered["date"], format="%d.%m.%Y").dt.day_name(locale="ru")

    weekend_days = ["Суббота", "Воскресенье"]
    filtered["is_workday"] = ~filtered["weekday"].isin(weekend_days)

    workday_avg = abs(filtered[filtered["is_workday"]]["amount"].mean())
    weekend_avg = abs(filtered[~filtered["is_workday"]]["amount"].mean())

    result = {
        "workday_avg": round(workday_avg if not pd.isna(workday_avg) else 0, 2),
        "weekend_avg": round(weekend_avg if not pd.isna(weekend_avg) else 0, 2),
        "period_start": start_date.strftime("%d.%m.%Y"),
        "period_end": end_date.strftime("%d.%m.%Y"),
    }

    logger.info(f"Средние траты: рабочий день — {result['workday_avg']} руб., выходной — {result['weekend_avg']} руб.")
    return result


# ============================================================
# Пример использования
# ============================================================

if __name__ == "__main__":
    from data_loader import get_transactions

    transactions_list = get_transactions()
    df = pd.DataFrame(transactions_list)

    print("\n" + "=" * 60)
    print("1. Траты по категории 'Супермаркеты':")
    result1 = spending_by_category(df, "Супермаркеты", "31.12.2021")
    print(result1)

    print("\n" + "=" * 60)
    print("2. Средние траты по дням недели:")
    result2 = spending_by_weekday(df, "31.12.2021")
    print(result2)

    print("\n" + "=" * 60)
    print("3. Средние траты в рабочий и выходной день:")
    result3 = spending_by_workday(df, "31.12.2021")
    print(result3)
