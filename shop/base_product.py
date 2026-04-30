class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description   # новое поле
        self.price = price
        self.quantity = quantity

    def __add__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(f"Нельзя складывать {type(self).__name__} с {type(other).__name__}")
        return (self.price * self.quantity) + (other.price * other.quantity)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, description={self.description[:20]}..., price={self.price}, quantity={self.quantity})"