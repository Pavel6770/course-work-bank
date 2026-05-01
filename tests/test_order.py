import pytest
from src.shop.product import Product
from src.shop.order import Order


def test_order_creation():
    p = Product("Товар", "desc", 100, 10)
    order = Order(p, 3)
    assert order.product == p
    assert order.quantity == 3
    assert order.total_price == 300


def test_order_str():
    p = Product("Товар", "desc", 100, 10)
    order = Order(p, 2)
    assert str(order) == "Заказ: Товар, 2 шт., итого: 200 руб."