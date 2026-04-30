from shop.product import Product
from shop.category import Category
from shop.loader import load_data_from_json


def main():
    print("Загрузка данных из JSON...")
    categories, products = load_data_from_json("products.json")

    print(f"Загружено категорий: {len(categories)}")
    print(f"Загружено продуктов: {len(products)}")

    for cat in categories:
        print(f"\nКатегория: {cat.name}")
        print(f"Описание: {cat.description}")
        print(f"Товаров в категории: {len(cat.products)}")

    print("\nПроверка сложения продуктов...")
    if len(products) >= 2:
        total = products[0] + products[1]
        print(f"Сумма первых двух продуктов: {total} руб.")


if __name__ == "__main__":
    main()