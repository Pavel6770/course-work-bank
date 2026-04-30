import pytest
from shop.smartphone import Smartphone
from shop.lawn_grass import LawnGrass
from shop.category import Category


def test_smartphone_attributes():
    phone = Smartphone("Xiaomi", 30000, 2, "Snapdragon", "12 Lite", 128, "Blue")
    assert phone.efficiency == "Snapdragon"
    assert phone.model == "12 Lite"
    assert phone.memory == 128
    assert phone.color == "Blue"


def test_lawn_grass_attributes():
    grass = LawnGrass("Трава", 500, 20, "Германия", 10, "Зелёный")
    assert grass.country == "Германия"
    assert grass.germination_period == 10
    assert grass.color == "Зелёный"


def test_add_same_class():
    phone1 = Smartphone("A", 1000, 1, "E1", "M1", 64, "Black")
    phone2 = Smartphone("B", 2000, 1, "E2", "M2", 128, "White")
    assert (phone1 + phone2) == 3000


def test_add_different_classes_raises_typeerror():
    phone = Smartphone("A", 1000, 1, "E1", "M1", 64, "Black")
    grass = LawnGrass("G", 500, 1, "RU", 7, "Green")
    with pytest.raises(TypeError):
        _ = phone + grass


def test_category_add_product():
    cat = Category("Test")
    phone = Smartphone("X", 1000, 1, "E", "M", 64, "Red")
    cat.add_product(phone)
    assert len(cat.products) == 1


def test_category_add_invalid_product():
    cat = Category("Test")
    with pytest.raises(TypeError):
        cat.add_product("not a product")

def test_product_repr():
    from shop.base_product import Product
    p = Product("Test", 100, 2)
    assert repr(p) == "Product(name=Test, price=100, quantity=2)"


def test_category_total_price():
    cat = Category("TestCat")
    p1 = Smartphone("A", 1000, 2, "E1", "M1", 64, "Black")
    p2 = LawnGrass("G", 500, 3, "RU", 7, "Green")
    cat.add_product(p1)
    cat.add_product(p2)
    # 1000*2 + 500*3 = 2000 + 1500 = 3500
    assert cat.total_price() == 3500.0


def test_add_product_invalid_type():
    cat = Category("TestCat")
    with pytest.raises(TypeError) as exc_info:
        cat.add_product(12345)
    assert "Можно добавлять только объекты Product" in str(exc_info.value)


def test_add_different_classes_error_message():
    phone = Smartphone("A", 1000, 1, "E1", "M1", 64, "Black")
    grass = LawnGrass("G", 500, 1, "RU", 7, "Green")
    with pytest.raises(TypeError) as exc_info:
        _ = phone + grass
    assert "Нельзя складывать" in str(exc_info.value)