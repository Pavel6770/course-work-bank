import pytest
from src.shop.product import Product
from src.shop.smartphone import Smartphone
from src.shop.lawn_grass import LawnGrass
from src.shop.category import Category


def test_smartphone_creation():
    phone = Smartphone("Phone", "Desc", 1000, 5, "Efficient", "Model X", 128, "Black")
    assert phone.efficiency == "Efficient"
    assert phone.model == "Model X"
    assert phone.memory == 128
    assert phone.color == "Black"


def test_lawn_grass_creation():
    grass = LawnGrass("Grass", "Desc", 500, 10, "Russia", 14, "Green")
    assert grass.country == "Russia"
    assert grass.germination_period == 14
    assert grass.color == "Green"


def test_add_same_class():
    phone1 = Smartphone("A", "desc", 1000, 1, "E", "M1", 64, "Black")
    phone2 = Smartphone("B", "desc", 2000, 1, "E", "M2", 128, "White")
    assert (phone1 + phone2) == 3000


def test_add_different_classes_raises_typeerror():
    phone = Smartphone("A", "desc", 1000, 1, "E", "M1", 64, "Black")
    grass = LawnGrass("G", "desc", 500, 1, "RU", 7, "Green")
    with pytest.raises(TypeError):
        _ = phone + grass


def test_add_product_to_category():
    cat = Category("TestCat", "desc", [])
    phone = Smartphone("P", "desc", 100, 2, "E", "M", 64, "Red")
    cat.add_product(phone)
    assert len(cat._products) == 1