import streamlit as st
import requests
import os

# Page config
st.set_page_config(page_title="DD Hospital Chatbot", layout="centered")
st.title("DD Hospital Chatbot - Streamlit UI")

# Backend URL
BACKEND_URL = os.getenv("BACKEND_URL", "https://dd-hospital-chatbot.onrender.com")

# Chat input
user_msg = st.text_input("Type your message:")

if st.button("Send"):
    if not user_msg.strip():
        st.warning("Please type a message!")
    else:
        try:
            # Call backend /chat endpoint
            resp = requests.post(f"{BACKEND_URL}/chat", json={"message": user_msg}, timeout=5)
            bot_reply = resp.json().get("reply", "No reply")
            st.success(bot_reply)
        except Exception as e:
            st.error("Backend not reachable: " + str(e))

# Health check (optional)
if st.button("Check backend health"):
    try:
        resp = requests.get(f"{BACKEND_URL}/health", timeout=5)
        st.json(resp.json())
    except Exception as e:
        st.error("Backend not reachable: " + str(e))
