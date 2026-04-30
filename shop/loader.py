import json
from shop.product import Product
from shop.category import Category


def load_data_from_json(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    products = []
    categories_dict = {}

    for item in data:
        product = Product(
            name=item["name"],
            description=item["description"],
            price=item["price"],
            quantity=item["quantity"]
        )
        products.append(product)

        cat_name = item["category"]
        if cat_name not in categories_dict:
            categories_dict[cat_name] = Category(
                name=cat_name,
                description=item["category_description"],
                products=[]
            )
        categories_dict[cat_name].products.append(product)

    return list(categories_dict.values()), products