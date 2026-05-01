import pytest
from src.shop.product import Product


def test_product_price_setter_negative():
    p = Product("A", "d", 100, 5)
    with pytest.raises(ValueError):
        p.price = -10


def test_product_quantity_setter_negative():
    p = Product("A", "d", 100, 5)
    with pytest.raises(ValueError):
        p.quantity = -1


def test_product_new_product():
    p = Product.new_product({"name": "X", "description": "desc", "price": 200, "quantity": 3})
    assert p.name == "X"
    assert p.price == 200
    assert p.quantity == 3


def test_product_new_product_with_duplicate():
    existing = [Product("X", "d", 100, 5)]
    p = Product.new_product({"name": "X", "description": "d", "price": 90, "quantity": 2}, existing)
    assert p.price == 100
    assert p.quantity == 7
    assert len(existing) == 0


def test_product_repr():
    p = Product("A", "long description", 100, 5)
    assert "A" in repr(p)
    assert "100" in repr(p)