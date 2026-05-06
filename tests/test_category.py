import pytest
from src.category import Category
from src.product import Product


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


def test_category_total_price():
    p1 = Product("A", "d", 100, 2)
    p2 = Product("B", "d", 200, 3)
    cat = Category("Cat", "desc", [p1, p2])
    assert cat.total_price() == 100*2 + 200*3


def test_category_products_getter():
    p = Product("Phone", "desc", 50000, 2)
    cat = Category("Cat", "desc", [p])
    assert "Phone" in cat.products


def test_category_add_product_invalid():
    cat = Category("Cat", "desc", [])
    with pytest.raises(TypeError):
        cat.add_product("not a product")


def test_category_add_product_success(capsys):
    cat = Category("Cat", "desc", [])
    p = Product("Test", "desc", 100, 5)
    cat.add_product(p)
    assert len(cat._products) == 1
    captured = capsys.readouterr()
    assert "успешно добавлен" in captured.out
    assert "Обработка добавления товара завершена" in captured.out


def test_category_average_price():
    cat = Category("Cat", "desc", [])
    assert cat.average_price() == 0.0
    p1 = Product("A", "desc", 100, 1)
    p2 = Product("B", "desc", 200, 1)
    cat.add_product(p1)
    cat.add_product(p2)
    assert cat.average_price() == 150.0