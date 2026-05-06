import pytest
from src.category import Category
from src.product import Product


def test_product_creation():
    p = Product("Test", "desc", 100, 5)
    assert p.name == "Test"
    assert p.price == 100
    assert p.quantity == 5


def test_product_price_setter():
    p = Product("Test", "desc", 100, 5)
    p.price = 200
    assert p.price == 200


def test_product_price_setter_negative():
    p = Product("Test", "desc", 100, 5)
    with pytest.raises(ValueError):
        p.price = -10


def test_product_quantity_setter():
    p = Product("Test", "desc", 100, 5)
    p.quantity = 10
    assert p.quantity == 10


def test_product_quantity_setter_negative():
    p = Product("Test", "desc", 100, 5)
    with pytest.raises(ValueError):
        p.quantity = -5


def test_product_zero_quantity():
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Zero", "desc", 100, 0)


def test_product_str():
    p = Product("Phone", "desc", 50000, 2)
    assert "Phone" in str(p)
    assert "50000" in str(p)


def test_product_add():
    p1 = Product("A", "d", 100, 2)
    p2 = Product("B", "d", 200, 1)
    assert (p1 + p2) == 400


def test_product_repr():
    p = Product("Test", "Very long description here", 100, 5)
    assert "Test" in repr(p)
    assert "description" in repr(p)