class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self._quantity = quantity

    @property
    def price(self) -> float:
        return self.__price

    @classmethod
    def new_product(cls, name, description, price, quantity, existing_products=None):
        if existing_products:
            for prod in existing_products:
                if prod.name == name:
                    price = max(price, prod.price)
                    quantity += prod.quantity
                    existing_products.remove(prod)
                    break
        return cls(name, description, price, quantity)

    @price.setter
    def price(self, value: float):
        if value <= 0:
            raise ValueError("Цена не должна быть нулевая или отрицательная")
        if value < self.__price:
            confirm = input(f"Цена понижается с {self.__price} до {value}. Подтвердить? (y/n): ").lower()
            if confirm != 'y':
               print("Изменение цены отменено")
               return
        self.__price = value

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        if value < 0:
            raise ValueError("Количество не может быть отрицательным")
        self._quantity = value

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(f"Нельзя складывать {type(self).__name__} с {type(other).__name__}")
        return (self.price * self.quantity) + (other.price * other.quantity)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, description={self.description[:30]}..., price={self.price}, quantity={self.quantity})"