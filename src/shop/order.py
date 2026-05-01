from src.shop.abstract_classes import BaseProduct
from src.shop.product import Product


class Order:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
        self.total_price = product.price * quantity

    def __str__(self):
        return f"Заказ: {self.product.name}, {self.quantity} шт., итого: {self.total_price} руб."