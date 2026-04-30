from typing import List
from shop.product import Product


class CategoryIterator:
    def __init__(self, category):
        self._products = category.products
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._products):
            raise StopIteration
        product = self._products[self._index]
        self._index += 1
        return product


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self._products = products

        Category.category_count += 1
        Category.product_count += len(products)

    @property
    def products(self):
        return self._products.copy()

    @property
    def products(self) -> List[Product]:
        return self._products.copy()

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product")
        self._products.append(product)
        Category.product_count += 1

    def __str__(self):
        total_quantity = sum(p.quantity for p in self._products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        return CategoryIterator(self)

    def total_price(self) -> float:
        return sum(p.price * p.quantity for p in self._products)