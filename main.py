from src.shop.product import Product
from src.shop.category import Category


def main():
    p1 = Product("Ноутбук", "Игровой ноутбук", 1500.99, 5)
    print(p1)

    cat = Category("Электроника", "Гаджеты", [p1])
    print(cat)
    print(cat.products)


if __name__ == "__main__":
    main()