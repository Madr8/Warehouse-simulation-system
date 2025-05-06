import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from inventory import Inventory
from workers import Worker
from orders import Order
from ws_listener import start_listener_thread

start_listener_thread()

if "inventory" not in st.session_state:
    st.session_state.inventory = Inventory()
    st.session_state.inventory.add_item("SKU123", 100)
    st.session_state.inventory.add_item("SKU456", 150)

if "worker1" not in st.session_state:
    st.session_state.worker1 = Worker(1)
    st.session_state.worker1.assign_task(Order("SKU123", 5))

if "worker2" not in st.session_state:
    st.session_state.worker2 = Worker(2)
    st.session_state.worker2.assign_task(Order("SKU456", 3))
    st.session_state.worker2.assign_task(Order("SKU123", 2))

if "order_log" not in st.session_state:
    st.session_state.order_log = [
        (Order("SKU123", 5), "Success"),
        (Order("SKU456", 3), "Success"),
        (Order("SKU123", 10), "Failed"),
    ]

inventory = st.session_state.inventory
worker1 = st.session_state.worker1
worker2 = st.session_state.worker2
order_log = st.session_state.order_log

st.title("📦 Warehouse Inventory Dashboard")

if st.button("🔁 Reset System"):
    st.session_state.clear()
    try:
        st.experimental_rerun()
    except:
        st.warning("System reset! Please manually refresh the page.")

st.subheader("📣 Notifications")
try:
    with open("realtime_notifications.log", "r") as f:
        logs = f.readlines()[-5:]
        for line in logs:
            st.warning(line.strip())
except FileNotFoundError:
    st.write("Waiting for live data...")

st.subheader("Current Inventory")
inv_data = inventory.get_inventory()
for sku, qty in inv_data.items():
    st.write(f"**{sku}**: {qty} units")

st.subheader("🔄 Restock Inventory")
restock_sku = st.selectbox("Select SKU to restock", list(inv_data.keys()))
restock_qty = st.number_input("Quantity to add", min_value=1, step=1)
if st.button("Restock"):
    inventory.restock_item(restock_sku, restock_qty)
    st.success(f"Restocked {restock_qty} units of {restock_sku}")

st.subheader("➕ Add New Inventory Item")
new_sku = st.text_input("Enter new SKU")
new_qty = st.number_input("Enter starting quantity", min_value=1, step=1, key="new_qty")
if st.button("Add SKU"):
    if new_sku:
        inventory.add_item(new_sku, new_qty)
        st.success(f"Added {new_qty} units of {new_sku}")
    else:
        st.error("Please enter a valid SKU name.")

st.subheader("🕒 Simulate Order")
if inventory.get_inventory():
    simulate_sku = st.selectbox("Select SKU for order", list(inventory.get_inventory().keys()), key="sim_sku")
    simulate_qty = st.number_input("Order quantity", min_value=1, step=1, key="sim_qty")
    simulate_worker = st.selectbox("Assign to Worker", [1, 2], key="sim_worker")

    if st.button("Simulate Order"):
        order = Order(simulate_sku, simulate_qty)
        assigned_worker = worker1 if simulate_worker == 1 else worker2
        if inventory.remove_item(order.sku, order.quantity):
            assigned_worker.assign_task(order)
            order_log.append((order, "Success"))
            st.success(f"Order for {simulate_qty} x {simulate_sku} assigned to Worker {simulate_worker}")
        else:
            order_log.append((order, "Failed"))
            st.error(f"Failed to place order for {simulate_qty} x {simulate_sku} — not enough inventory.")

st.subheader("👷 Worker Performance")
for worker in [worker1, worker2]:
    st.write(f"### Worker {worker.worker_id}")
    st.write(f"Tasks Completed: {worker.get_tasks_completed()}")
    for task in worker.get_task_log():
        st.markdown(f"- {task}")

st.subheader("📋 Order Log")
order_data = {
    "SKU": [order.sku for order, _ in order_log],
    "Quantity": [order.quantity for order, _ in order_log],
    "Status": [status for _, status in order_log],
    "Timestamp": [order.timestamp.strftime("%Y-%m-%d %H:%M:%S") for order, _ in order_log],
}
order_df = pd.DataFrame(order_data)
st.dataframe(order_df)

st.subheader("📉 Inventory Level Chart")
skus = list(inv_data.keys())
quantities = [inv_data[sku] for sku in skus]
fig, ax = plt.subplots()
ax.bar(skus, quantities, color='skyblue')
ax.set_ylabel("Units Remaining")
ax.set_title("Inventory Levels by SKU")
st.pyplot(fig)

st.markdown("---")
st.caption("Smart Warehouse Simulator | Streamlit + WebSocket Notifications")
