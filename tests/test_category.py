import pytest
from src.shop.product import Product
from src.shop.category import Category


def test_average_price():
    p1 = Product("A", "desc", 100, 1)
    p2 = Product("B", "desc", 200, 1)
    cat = Category("Test", "desc", [p1, p2])
    assert cat.average_price() == 150.0


def test_average_price_empty():
    cat = Category("Empty", "desc", [])
    assert cat.average_price() == 0.0


def test_add_product_zero_quantity():
    cat = Category("TestCat", "desc", [])
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Zero", "desc", 100, 0)

def test_add_product_success(capsys):
    cat = Category("TestCat", "desc", [])
    p = Product("Normal", "desc", 100, 5)
    cat.add_product(p)
    captured = capsys.readouterr()
    assert "успешно добавлен" in captured.out
    assert "Обработка добавления товара завершена" in captured.out