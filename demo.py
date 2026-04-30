from shop.product import Product
from shop.category import Category


def main():
    print("=== Создаём продукты ===")
    p1 = Product("Ноутбук", "Игровой ноутбук", 1500.99, 5)
    p2 = Product("Мышь", "Беспроводная мышь", 25.50, 10)

    print(p1)
    print(p2)

    print("\n=== Создаём категорию ===")
    cat = Category("Электроника", "Гаджеты и устройства", [p1, p2])
    print(cat)

    print(f"\nОбщая стоимость категории: {cat.total_price()} руб.")
    print(f"Сумма продуктов (p1 + p2): {p1 + p2} руб.")

    print("\n=== Проверка сеттеров с валидацией ===")
    try:
        p1.price = -100
    except ValueError as e:
        print(f"Ошибка при установке цены: {e}")

    try:
        p1.quantity = -5
    except ValueError as e:
        print(f"Ошибка при установке количества: {e}")

    print("\n=== Проверка добавления продукта в категорию ===")
    p3 = Product("Клавиатура", "Механическая", 120.00, 3)
    cat.add_product(p3)
    print(f"После добавления: {cat}")
    print(f"Общая стоимость обновлённой категории: {cat.total_price()} руб.")

    print("\n=== Проверка итерации по категории ===")
    for product in cat:
        print(f"  - {product}")


if __name__ == "__main__":
    main()