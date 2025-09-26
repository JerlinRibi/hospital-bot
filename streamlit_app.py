# streamlit_app.py

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# -----------------------
# Data files
# -----------------------
CHATLOG_FILE = "chatlogs.csv"
APPOINTMENT_FILE = "appointments.csv"

# Create files if they don't exist
if not os.path.exists(CHATLOG_FILE):
    pd.DataFrame(columns=["timestamp", "message", "reply"]).to_csv(CHATLOG_FILE, index=False)

if not os.path.exists(APPOINTMENT_FILE):
    pd.DataFrame(columns=["timestamp", "name", "date", "time"]).to_csv(APPOINTMENT_FILE, index=False)

# -----------------------
# FAQ
# -----------------------
FAQ = {
    "fever": "Please take rest and drink fluids.",
    "headache": "Take some rest and stay hydrated.",
    "appointment": "You can book an appointment below.",
    "doctor": "Our doctors are available Mon-Fri, 9AM-5PM.",
    "working hours": "Our hospital is open Mon-Fri 9AM-5PM.",
    "contact": "Call us at +91-XXXXXXXX",
    "hospital info": "DD Hospital is located at Main Street.",
    "emergency": "For emergency, call 108 immediately.",
    "insurance": "We accept most major insurance providers."
}

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(page_title="DD Hospital Chatbot", layout="centered")
st.title("DD Hospital Chatbot - Simple UI")

# --- Chat Section ---
st.subheader("Chat with Bot")
user_msg = st.text_input("Type your message:")

if st.button("Send"):
    if user_msg.strip() == "":
        st.warning("Please type a message!")
    else:
        text = user_msg.lower()
        reply = "Sorry, I didn’t understand. Please ask about appointments, doctors, or hospital info."
        for key in FAQ:
            if key in text:
                reply = FAQ[key]
                break
        st.success(reply)

        # Save chatlog
        df = pd.read_csv(CHATLOG_FILE)
        df = pd.concat([df, pd.DataFrame([[datetime.now(), user_msg, reply]], columns=df.columns)], ignore_index=True)
        df.to_csv(CHATLOG_FILE, index=False)

# --- Appointment Section ---
st.subheader("Book an Appointment")
name = st.text_input("Your Name")
date = st.date_input("Appointment Date")
time_input = st.text_input("Time (e.g., 10:00 AM)")

if st.button("Book Appointment"):
    if name.strip() == "" or time_input.strip() == "":
        st.warning("Please enter name and time")
    else:
        df_appt = pd.read_csv(APPOINTMENT_FILE)
        df_appt = pd.concat([df_appt, pd.DataFrame([[datetime.now(), name, str(date), time_input]], columns=df_appt.columns)], ignore_index=True)
        df_appt.to_csv(APPOINTMENT_FILE, index=False)
        st.success(f"Appointment booked for {name} on {date} at {time_input}")

# --- Optional: Show last 5 chatlogs ---
st.subheader("Last 5 Chat Logs")
chat_df = pd.read_csv(CHATLOG_FILE)
st.table(chat_df.tail(5))
