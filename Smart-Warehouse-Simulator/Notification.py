import streamlit as st

def show_notification():
    st.toast("🚨 New Order Received! 🚨")
    st.balloons()  # Simulate pop-out effect

# Simulate a notification
show_notification()
