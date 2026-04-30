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


def test_category_initialization(sample_category, sample_product):
    assert sample_category.name == "Электроника"
    assert sample_category.description == "Смартфоны, ноутбуки"
    assert len(sample_category.products) == 1
    assert sample_category.products[0] == sample_product


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

def test_category_iterator(sample_category, sample_product):
    products = [p for p in sample_category]
    assert len(products) == 1
    assert products[0] == sample_product