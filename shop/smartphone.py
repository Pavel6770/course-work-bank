from models.product import Product


class Smartphone(Product):
    def __init__(self, name: str, price: float, quantity: int, efficiency: str, model: str, memory: int, color: str):
        super().__init__(name, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color
