from src.shop.abstract_classes import BaseProduct
from src.shop.mixins import LogMixin


class Product(BaseProduct, LogMixin):
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self._quantity = quantity
        super().__init__(name, description, price, quantity)

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float):
        if value <= 0:
            raise ValueError("Цена не должна быть нулевая или отрицательная")
        self.__price = value

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        if value < 0:
            raise ValueError("Количество не может быть отрицательным")
        self._quantity = value

    @classmethod
    def new_product(cls, product_data: dict, existing_products=None):
        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        if existing_products:
            for prod in existing_products:
                if prod.name == name:
                    price = max(price, prod.price)
                    quantity += prod.quantity
                    existing_products.remove(prod)
                    break
        return cls(name, description, price, quantity)

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError(f"Нельзя складывать {type(self).__name__} с {type(other).__name__}")
        return (self.price * self.quantity) + (other.price * other.quantity)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, description={self.description[:30]}..., price={self.price}, quantity={self.quantity})"