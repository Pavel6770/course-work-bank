import pytest
from src.shop.product import Product
from src.shop.abstract_classes import BaseProduct


def test_base_product_abstract():
    with pytest.raises(TypeError):
        BaseProduct()


def test_mixin_logging(capsys):
    p = Product("Тест", "Описание", 100, 5)
    captured = capsys.readouterr()
    assert "Создан Product с параметрами" in captured.out