# ws_listener.py
import websocket
import json
import streamlit as st  # optional if integrating directly
import threading

def on_message(ws, message):
    data = json.loads(message)
    print("🔔 Notification Received:", data)

    # Optional: Save to file or database
    with open("realtime_notifications.log", "a") as f:
        f.write(json.dumps(data) + "\n")

def on_error(ws, error):
    print("❗ Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("🔌 WebSocket Closed")

def on_open(ws):
    print("✅ Connected to WebSocket API")
    # Optional: Send authentication message or subscribe to topics
    # ws.send(json.dumps({"type": "auth", "token": "YOUR_TOKEN"}))

def run_websocket():
    ws_url = "wss://api.yourcompany.com/notifications"  # replace with actual
    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    ws.run_forever()

# To run it in the background
def start_listener_thread():
    thread = threading.Thread(target=run_websocket)
    thread.daemon = True
    thread.start()
