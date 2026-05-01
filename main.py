from src.shop.product import Product
from src.shop.smartphone import Smartphone
from src.shop.lawn_grass import LawnGrass
from src.shop.category import Category


def main():
    print("=== 1. Создание продуктов ===\n")

    # Обычный продукт
    laptop = Product("Ноутбук", "Игровой ноутбук", 1500.99, 5)
    print(laptop)

    # Смартфон
    phone = Smartphone(
        name="iPhone 15",
        description="Флагман Apple",
        price=120000,
        quantity=10,
        efficiency="A17 Pro",
        model="15 Pro",
        memory=256,
        color="Silver"
    )
    print(phone)

    # Газонная трава
    grass = LawnGrass(
        name="Изумруд",
        description="Газонная трава",
        price=1500,
        quantity=20,
        country="Россия",
        germination_period=14,
        color="Зелёный"
    )
    print(grass)

    print("\n=== 2. Сложение продуктов ===\n")
    # Складываем два смартфона
    phone2 = Smartphone("Samsung", "Флагман", 110000, 5, "Snapdragon", "S24", 512, "Black")
    total_price = phone + phone2
    print(f"Сумма двух смартфонов: {total_price} руб.")

    # Попытка сложить смартфон и траву (должна быть ошибка)
    try:
        result = phone + grass
    except TypeError as e:
        print(f"Ошибка (ожидаемо): {e}")

    print("\n=== 3. Категория и добавление товаров ===\n")
    electronics = Category("Электроника", "Гаджеты", [laptop, phone])
    print(electronics)
    print("Товары в категории:\n", electronics.products)

    # Добавляем ещё один смартфон
    electronics.add_product(phone2)
    print(f"\nПосле добавления: {electronics}")
    print("Обновлённый список:\n", electronics.products)

    print("\n=== 4. Итерация по категории ===\n")
    for product in electronics:
        print(f"  - {product}")


if __name__ == "__main__":
    main()