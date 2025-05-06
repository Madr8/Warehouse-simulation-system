from inventory import Inventory
from orders import OrderGenerator
from workers import Worker

# Initialize components
inventory = Inventory()
inventory.add_item("SKU123", 100)
inventory.add_item("SKU456", 150)

order_gen = OrderGenerator(["SKU123", "SKU456"])
workers = [Worker(1), Worker(2)]

order_log = []

# Simulate 5 orders with alternating workers
for i in range(5):
    order = order_gen.generate_order()
    assigned_worker = workers[i % len(workers)]
    if inventory.remove_item(order.sku, order.quantity):
        assigned_worker.assign_task(order)
        order_log.append((order, "Success"))
    else:
        print(f"Not enough inventory for {order.sku}")
        order_log.append((order, "Failed"))

print("\nFinal Inventory:")
print(inventory.get_inventory())