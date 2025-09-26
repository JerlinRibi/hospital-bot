import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="DD Hospital Chatbot", page_icon="🏥")

st.title("🏥 DD Hospital Chatbot")

# ----------------- Sidebar -----------------
st.sidebar.title("Navigation")
option = st.sidebar.selectbox(
    "Go to",
    ["Chatbot", "Book Appointment", "View Appointments", "View Chat Logs"]
)

# ----------------- Backend URL -----------------
BASE_URL = "http://127.0.0.1:8000"  # Change if deployed to online FastAPI

# ----------------- Chatbot -----------------
if option == "Chatbot":
    st.subheader("Chat with Bot")
    msg = st.text_input("Type your message:")
    if st.button("Send"):
        if msg.strip() != "":
            try:
                response = requests.post(f"{BASE_URL}/chat", json={"message": msg})
                st.write(response.json()["reply"])
            except:
                st.error("Error connecting to chatbot. Make sure FastAPI server is running.")

# ----------------- Book Appointment -----------------
elif option == "Book Appointment":
    st.subheader("Book an Appointment")
    with st.form("appointment_form"):
        name = st.text_input("Your Name")
        date = st.date_input("Select Date")
        time = st.text_input("Select Time (e.g., 10:00 AM)")
        submitted = st.form_submit_button("Book Appointment")
        if submitted:
            try:
                payload = {"patient_name": name, "date": str(date), "time": time}
                response = requests.post(f"{BAS
