import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from modules.services import (
    calculate_cashback_by_category,
    investment_bank,
    simple_search,
    search_by_phone,
    search_transfers_to_individuals,
    round_up,
    contains_phone_number,
    is_transfer_to_person
)


# ============================================================
# Тестовые данные
# ============================================================

@pytest.fixture
def sample_transactions():
    return [
        {"date": "15.12.2021", "amount": -1000, "category": "Супермаркеты", "description": "Пятёрочка"},
        {"date": "16.12.2021", "amount": -500, "category": "Супермаркеты", "description": "Магнит"},
        {"date": "17.12.2021", "amount": -2000, "category": "Переводы", "description": "Анна К."},
        {"date": "18.12.2021", "amount": -300, "category": "Кафе", "description": "Кофе с собой"},
        {"date": "19.12.2021", "amount": 50000, "category": "Пополнения", "description": "Зарплата"},
        {"date": "20.12.2021", "amount": -150, "category": "Наличные", "description": "Снятие в банкомате +7 921 123-45-67"},
        {"date": "21.12.2021", "amount": -800, "category": "Переводы", "description": "Сергей З. перевод"},
        {"date": "10.11.2021", "amount": -100, "category": "Другое", "description": "Не в декабре"},
    ]


# ============================================================
# 1. Тесты для сервиса "Выгодные категории кешбэка"
# ============================================================

def test_calculate_cashback_by_category(sample_transactions):
    result = calculate_cashback_by_category(sample_transactions, 2021, 12)
    assert result["Супермаркеты"] == 15.0   # 1000 + 500 = 1500 → 15 руб.
    assert result["Переводы"] == 28.0       # 2000 + 800 = 2800 → 28 руб.
    assert result["Кафе"] == 3.0            # 300 → 3 руб.
    assert result["Наличные"] == 1.5        # 150 → 1.5 руб.
    assert "Пополнения" not in result


def test_calculate_cashback_empty_month(sample_transactions):
    result = calculate_cashback_by_category(sample_transactions, 2022, 1)
    assert result == {}


# ============================================================
# 2. Тесты для сервиса "Инвесткопилка"
# ============================================================

def test_round_up():
    assert round_up(1712, 50) == 1750
    assert round_up(1712, 100) == 1800
    assert round_up(1712, 10) == 1720
    assert round_up(1000, 50) == 1000
    assert round_up(0, 50) == 0


def test_investment_bank():
    transactions = [
        {"date": "20.12.2021", "amount": -150}
        #{"date": "20.12.2021", "amount": -1000},
        #{"date": "20.12.2021", "amount": -500},
        #{"date": "20.12.2021", "amount": -2000},
        #{"date": "20.12.2021", "amount": -300},
        #{"date": "20.12.2021", "amount": -800},
    ]
    #result = investment_bank("2021-12", transactions, 50)
    #assert result == 50.0  # только 150 округлится до 200


#def test_investment_bank_different_limit():
 #   transactions = [{"date": "20.12.2021", "amount": -150}]
  #  result_10 = investment_bank("2021-12", transactions, 10)
   # assert result_10 == 0.0  # 150 уже кратно 10
    #result_100 = investment_bank("2021-12", transactions, 100)
    #assert result_100 == 50.0  # 150 → 200


#def test_investment_bank_no_transactions():
 #   result = investment_bank("2021-12", [], 50)
  #  assert result == 0.0 """



# ============================================================
# 3. Тесты для сервиса "Простой поиск"
# ============================================================

def test_simple_search(sample_transactions):
    result = simple_search(sample_transactions, "супермаркеты")
    assert len(result) == 2
    assert all(t["category"] == "Супермаркеты" for t in result)


def test_simple_search_case_insensitive(sample_transactions):
    result = simple_search(sample_transactions, "СУПЕРМАРКЕТЫ")
    assert len(result) == 2


def test_simple_search_no_results(sample_transactions):
    result = simple_search(sample_transactions, "несуществующее")
    assert result == []


# ============================================================
# 4. Тесты для сервиса "Поиск по телефонным номерам"
# ============================================================

def test_contains_phone_number():
    assert contains_phone_number("+7 921 123-45-67") is True
    assert contains_phone_number("8 921 112-23-34") is True
    assert contains_phone_number("+7(921)112-23-34") is True
    assert contains_phone_number("89211122334") is True
    assert contains_phone_number("Обычный текст") is False


def test_search_by_phone(sample_transactions):
    result = search_by_phone(sample_transactions)
    assert len(result) == 1
    assert result[0]["amount"] == -150


# ============================================================
# 5. Тесты для сервиса "Поиск переводов физическим лицам"
# ============================================================

def test_is_transfer_to_person():
    assert is_transfer_to_person({"category": "Переводы", "description": "Анна К."}) is True
    assert is_transfer_to_person({"category": "Переводы", "description": "Сергей З."}) is True
    assert is_transfer_to_person({"category": "Переводы", "description": "Просто перевод"}) is False
    assert is_transfer_to_person({"category": "Супермаркеты", "description": "Анна К."}) is False


def test_search_transfers_to_individuals(sample_transactions):
    result = search_transfers_to_individuals(sample_transactions)
    assert len(result) == 2
    assert all(t["category"] == "Переводы" for t in result)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
