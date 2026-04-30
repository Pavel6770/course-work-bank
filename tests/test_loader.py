import pytest
import json
import tempfile
from shop.loader import load_data_from_json


def test_load_data_from_json():
    json_content = '''
    [
      {
        "name": "Товар 1",
        "description": "Описание 1",
        "price": 100.0,
        "quantity": 5,
        "category": "Категория A",
        "category_description": "Описание категории A"
      },
      {
        "name": "Товар 2",
        "description": "Описание 2",
        "price": 200.0,
        "quantity": 3,
        "category": "Категория A",
        "category_description": "Описание категории A"
      }
    ]
    '''

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as tmp:
        tmp.write(json_content)
        tmp_path = tmp.name

    categories, products = load_data_from_json(tmp_path)

    assert len(products) == 2
    assert products[0].name == "Товар 1"
    assert products[0].price == 100.0
    assert products[0].quantity == 5

    assert len(categories) == 1
    assert categories[0].name == "Категория A"
    assert len(categories[0].products) == 2


def test_load_data_from_json_empty():
    json_content = '[]'

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as tmp:
        tmp.write(json_content)
        tmp_path = tmp.name

    categories, products = load_data_from_json(tmp_path)

    assert len(products) == 0
    assert len(categories) == 0