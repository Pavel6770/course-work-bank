from models.product import Product

class LawnGrass(Product):
    def __init__(self, name: str, price: float, quantity: int,
                 country: str, germination_period: int, color: str):
        super().__init__(name, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color