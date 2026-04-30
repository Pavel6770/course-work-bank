import pytest
from shop.product import Product
from shop.category import Category


@pytest.fixture
def sample_product():
    return Product("Ноутбук", "Мощный игровой ноутбук", 1500.99, 5)


@pytest.fixture
def sample_category(sample_product):
    return Category("Электроника", "Смартфоны, ноутбуки", [sample_product])


def test_product_initialization(sample_product):
    assert sample_product.name == "Ноутбук"
    assert sample_product.description == "Мощный игровой ноутбук"
    assert sample_product.price == 1500.99
    assert sample_product.quantity == 5


def test_product_price_setter():
    p = Product("Тест", "Описание", 100, 5)
    p.price = 200
    assert p.price == 200
    with pytest.raises(ValueError):
        p.price = -10


def test_product_quantity_setter():
    p = Product("Тест", "Описание", 100, 5)
    p.quantity = 10
    assert p.quantity == 10
    with pytest.raises(ValueError):
        p.quantity = -5


def test_category_initialization(sample_category, sample_product):
    assert sample_category.name == "Электроника"
    assert sample_category.description == "Смартфоны, ноутбуки"
    assert "Ноутбук" in sample_category.products
    assert "1500.99 руб." in sample_category.products
    assert "Остаток: 5 шт." in sample_category.products


def test_category_counters():
    Category.category_count = 0
    Category.product_count = 0

    p1 = Product("A", "desc1", 100, 2)
    p2 = Product("B", "desc2", 200, 3)

    Category("Cat1", "desc1", [p1])
    Category("Cat2", "desc2", [p2, p1])

    assert Category.category_count == 2
    assert Category.product_count == 3


def test_product_addition():
    p1 = Product("A", "descA", 100, 2)
    p2 = Product("B", "descB", 200, 1)
    assert (p1 + p2) == (100 * 2) + (200 * 1)


def test_product_str(sample_product):
    assert str(sample_product) == "Ноутбук, 1500.99 руб. Остаток: 5 шт."


def test_category_str(sample_category, sample_product):
    assert str(sample_category) == "Электроника, количество продуктов: 5 шт."


def test_category_add_product(sample_category, sample_product):
    old_count = Category.product_count
    sample_category.add_product(sample_product)
    assert sample_category.products.count("Ноутбук") == 2
    assert Category.product_count == old_count + 1


def test_category_iterator(sample_category, sample_product):
    products = list(sample_category)
    assert len(products) == 1
    assert products[0] == sample_product


def test_products_getter(sample_category):
    assert isinstance(sample_category.products, str)
    assert "Ноутбук" in sample_category.products
    assert "1500.99 руб." in sample_category.products


def test_new_product():
    p = Product.new_product("Тест", "Описание", 100, 5)
    assert p.name == "Тест"
    assert p.price == 100
    assert p.quantity == 5


def test_new_product_with_duplicate():
    existing = [
        Product("Ноутбук", "Описание", 1000, 5),
        Product("Мышь", "Описание", 50, 10)
    ]
    new = Product.new_product("Ноутбук", "Новое описание", 900, 3, existing)
    assert new.price == 1000
    assert new.quantity == 8
    assert len(existing) == 1
    assert existing[0].name == "Мышь"