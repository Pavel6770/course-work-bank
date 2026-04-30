from typing import List
from shop.base_product import Product


class Category:
    """
    Категория товаров.
    Позволяет добавлять только объекты, являющиеся наследниками Product.
    """

    def __init__(self, name: str):
        self.name = name
        self.products: List[Product] = []

    def add_product(self, product: Product) -> None:
        """
        Добавляет продукт в категорию только если это экземпляр Product или его наследник.
        """
        if not isinstance(product, Product):
            raise TypeError(f"Можно добавлять только объекты Product, передан {type(product).__name__}")
        self.products.append(product)

    def total_price(self) -> float:
        """
        Общая стоимость всех товаров в категории.
        """
        return sum(p.price * p.quantity for p in self.products)