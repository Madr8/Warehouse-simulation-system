# --- workers.py ---
class Worker:
    def __init__(self, worker_id):
        self.worker_id = worker_id
        self.tasks_completed = 0
        self.task_log = []

    def assign_task(self, order):
        task = f"Picked {order.quantity} of {order.sku}"
        self.task_log.append(task)
        self.tasks_completed += 1
        print(f"Worker {self.worker_id} assigned: {task}")

    def get_task_log(self):
        return self.task_log

    def get_tasks_completed(self):
        return self.tasks_completed