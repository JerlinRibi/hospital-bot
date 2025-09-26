import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "https://dd-hospital-chatbot.onrender.com")

user_msg = st.text_input("Type your message:")

if st.button("Send"):
    if user_msg.strip() == "":
        st.warning("Please type a message!")
    else:
        try:
            resp = requests.post(f"{BACKEND_URL}/chat", json={"message": user_msg}, timeout=5)
            st.success(resp.json().get("reply", "No reply"))
        except Exception as e:
            st.error("Backend not reachable: " + str(e))
