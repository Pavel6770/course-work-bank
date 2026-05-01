import pytest
from src.shop.smartphone import Smartphone
from src.shop.lawn_grass import LawnGrass
from src.shop.category import Category


def test_smartphone_creation():
    phone = Smartphone("Phone", "Desc", 1000, 5, "Eff", "Model", 128, "Black")
    assert phone.efficiency == "Eff"
    assert phone.model == "Model"
    assert phone.memory == 128
    assert phone.color == "Black"


def test_lawn_grass_creation():
    grass = LawnGrass("Grass", "Desc", 500, 10, "RU", 14, "Green")
    assert grass.country == "RU"
    assert grass.germination_period == 14
    assert grass.color == "Green"


def test_add_same_class():
    p1 = Smartphone("A", "d", 1000, 1, "E", "M", 64, "B")
    p2 = Smartphone("B", "d", 2000, 1, "E", "M", 128, "W")
    assert (p1 + p2) == 3000


def test_add_different_classes():
    phone = Smartphone("A", "d", 1000, 1, "E", "M", 64, "B")
    grass = LawnGrass("G", "d", 500, 1, "RU", 7, "G")
    with pytest.raises(TypeError):
        _ = phone + grass


def test_category_add_product():
    cat = Category("Test", "desc", [])
    phone = Smartphone("P", "d", 100, 2, "E", "M", 64, "R")
    cat.add_product(phone)
    assert len(cat._products) == 1