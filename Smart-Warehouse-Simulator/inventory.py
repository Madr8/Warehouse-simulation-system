# Smart Warehouse Simulator - Starter Code with Streamlit Dashboard

# --- inventory.py ---
class Inventory:
    def __init__(self):
        self.items = {}  # SKU: quantity

    def add_item(self, sku, quantity):
        self.items[sku] = self.items.get(sku, 0) + quantity

    def remove_item(self, sku, quantity):
        if self.items.get(sku, 0) >= quantity:
            self.items[sku] -= quantity
            return True
        return False

    def get_inventory(self):
        return self.items

    def restock_item(self, sku, quantity):
        self.add_item(sku, quantity)


