import asyncio
import websockets
import streamlit as st

async def listen_for_updates():
    uri = "ws://yourcompanysystem.com/real-time-updates"  # Replace with your system's WebSocket URL
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            st.toast(f"New Update: {message}")  # Display the real-time update

# Start WebSocket listener
asyncio.get_event_loop().run_until_complete(listen_for_updates())
