import streamlit as st
import requests
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from threading import Thread
import uvicorn

# ----------------- FastAPI Backend -----------------
app = FastAPI()

class Appointment(BaseModel):
    patient_name: str
    date: str
    time: str

class ChatRequest(BaseModel):
    message: str

FAQ = {
    "fever": "Please take rest and drink fluids.",
    "headache": "Take some rest and stay hydrated.",
    "appointment": "You can book an appointment using /appointment endpoint.",
    "doctor": "Our doctors are available Mon-Fri, 9AM-5PM."
}

appointments = []
chatlogs = []

@app.post("/appointment")
def create_appointment(appointment: Appointment):
    appointments.append({
        "patient_name": appointment.patient_name,
        "date": appointment.date,
        "time": appointment.time
    })
    return {"message": f"Appointment booked for {appointment.patient_name} on {appointment.date} at {appointment.time}"}

@app.post("/chat")
def chat(request: ChatRequest):
    text = request.message.lower()
    reply = "Sorry, I didn’t understand."
    for key in FAQ:
        if key in text:
            reply = FAQ[key]
            break
    chatlogs.append({"message": request.message, "reply": reply})
    return {"reply": reply}

@app.get("/appointments")
def get_appointments():
    return appointments

@app.get("/chatlogs")
def get_chatlogs():
    return chatlogs

# ----------------- Start FastAPI in Thread -----------------
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

thread = Thread(target=run_fastapi, daemon=True)
thread.start()

# ----------------- Streamlit UI -----------------
st.set_page_config(page_title="DD Hospital Chatbot", page_icon="🏥")
st.title("🏥 DD Hospital Chatbot")

option = st.sidebar.selectbox(
    "Go to",
    ["Chatbot", "Book Appointment", "View Appointments", "View Chat Logs"]
)

BASE_URL = "http://127.0.0.1:8000"

# Chatbot
if option == "Chatbot":
    msg = st.text_input("Type your message:")
    if st.button("Send"):
        if msg.strip() != "":
            response = requests.post(f"{BASE_URL}/chat", json={"message": msg})
            st.write(response.json()["reply"])

# Book Appointment
elif option == "Book Appointment":
    with st.form("appointment_form"):
        name = st.text_input("Your Name")
        date = st.date_input("Select Date")
        time = st.text_input("Select Time (e.g., 10:00 AM)")
        submitted = st.form_submit_button("Book Appointment")
        if submitted:
            payload = {"patient_name": name, "date": str(date), "time": time}
            response = requests.post(f"{BASE_URL}/appointment", json=payload)
            st.success(response.json()["message"])

# View Appointments
elif option == "View Appoint
