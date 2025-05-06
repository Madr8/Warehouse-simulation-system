from datetime import datetime

class Order:
    def __init__(self, sku, quantity):
        self.sku = sku
        self.quantity = quantity
        self.timestamp = datetime.now()  # Capture the timestamp when the order is created
