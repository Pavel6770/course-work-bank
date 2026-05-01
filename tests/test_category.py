import pytest
from src.shop.product import Product
from src.shop.category import Category


def test_category_creation():
    p = Product("A", "desc", 100, 2)
    cat = Category("Electronics", "Gadgets", [p])
    assert cat.name == "Electronics"
    assert cat.description == "Gadgets"
    assert len(cat._products) == 1


def test_category_add_product():
    # Сбрасываем счётчики перед тестом
    Category.category_count = 0
    Category.product_count = 0

    cat = Category("C", "desc", [])
    p1 = Product("A", "d", 100, 2)
    p2 = Product("B", "d", 200, 3)
    cat.add_product(p1)
    cat.add_product(p2)
    assert len(cat._products) == 2
    assert Category.product_count == 2


def test_category_str():
    p = Product("A", "desc", 100, 2)
    cat = Category("C", "desc", [p])
    assert str(cat) == "C, количество продуктов: 2 шт."


def test_category_total_price():
    p1 = Product("A", "d", 100, 2)
    p2 = Product("B", "d", 200, 3)
    cat = Category("C", "desc", [p1, p2])
    assert cat.total_price() == (100*2)+(200*3)


def test_category_products_getter(capsys):
    p = Product("A", "d", 100, 2)
    cat = Category("C", "desc", [p])
    print(cat.products)
    captured = capsys.readouterr()
    assert "A, 100 руб. Остаток: 2 шт." in captured.out


def test_category_total_price_empty():
    cat = Category("C", "desc", [])
    assert cat.total_price() == 0


def test_category_add_product_invalid():
    cat = Category("C", "desc", [])
    with pytest.raises(TypeError):
        cat.add_product("not a product")