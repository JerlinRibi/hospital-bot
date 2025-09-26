import streamlit as st
import requests
import os

st.set_page_config(page_title="DD Hospital Chatbot", layout="centered")
st.title("DD Hospital Chatbot - Streamlit UI")

BACKEND_URL = os.getenv("BACKEND_URL", "https://dd-hospital-chatbot.onrender.com")

user_msg = st.text_input("Type your message:")
if st.button("Send"):
    # Dummy echo
    st.write("Bot reply:", user_msg[::-1])

if st.button("Check backend health"):
    try:
        resp = requests.get(f"{BACKEND_URL}/health", timeout=3)
        st.json(resp.json())
    except Exception as e:
        st.error("Backend not reachable: " + str(e))
