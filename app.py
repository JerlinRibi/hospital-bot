import threading
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import streamlit as st
import requests

# -----------------------
# FastAPI App
# -----------------------
app = FastAPI(
    title="DD Hospital Chatbot",
    description="Simple hospital chatbot with appointment booking and symptom-based replies",
    version="1.0"
)

# -----------------------
# Pydantic Models
# -----------------------
class Appointment(BaseModel):
    patient_name: str
    date: str
    time: str

class ChatRequest(BaseModel):
    message: str

# -----------------------
# Database Setup
# -----------------------
Base = declarative_base()

class AppointmentDB(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String)
    date = Column(String)
    time = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ChatLogDB(Base):
    __tablename__ = "chatlogs"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    reply = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_engine("sqlite:///hospital.db")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -----------------------
# FAQ for Chatbot
# -----------------------
FAQ = {
    "fever": "Please take rest and drink fluids.",
    "headache": "Take some rest and stay hydrated.",
    "appointment": "You can book an appointment using /appointment endpoint.",
    "doctor": "Our doctors are available Mon-Fri, 9AM-5PM.",
    "working hours": "Our hospital is open Mon-Fri 9AM-5PM.",
    "contact": "Call us at +91-XXXXXXXX",
    "hospital info": "DD Hospital is located at Main Street.",
    "emergency": "For emergency, call 108 immediately.",
    "insurance": "We accept most major insurance providers."
}

# -----------------------
# FastAPI Endpoints
# -----------------------
@app.get("/hello")
def read_hello():
    return {"message": "Welcome to DD Hospital"}

@app.post("/appointment")
def create_appointment(appointment: Appointment):
    db = SessionLocal()
    db_appointment = AppointmentDB(
        patient_name=appointment.patient_name,
        date=appointment.date,
        time=appointment.time
    )
    db.add(db_appointment)
    db.commit()
    db.close()
    return {
        "message": f"Appointment booked for {appointment.patient_name} on {appointment.date} at {appointment.time}"
    }

@app.post("/chat")
def chat(request: ChatRequest):
    text = request.message.lower()
    reply = "Sorry, I didn’t understand. Please ask about appointments, doctors, or hospital info."
    for key in FAQ:
        if key in text:
            reply = FAQ[key]
            break

    db = SessionLocal()
    chat_log = ChatLogDB(message=request.message, reply=reply)
    db.add(chat_log)
    db.commit()
    db.close()

    return {"reply": reply}

@app.get("/appointments")
def get_appointments():
    db = SessionLocal()
    appointments = db.query(AppointmentDB).all()
    db.close()
    return appointments

@app.get("/chatlogs")
def get_chatlogs():
    db = SessionLocal()
    logs = db.query(ChatLogDB).all()
    db.close()
    return logs

# -----------------------
# Run FastAPI in thread
# -----------------------
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

threading.Thread(target=run_fastapi, daemon=True).start()

# -----------------------
# Streamlit Frontend
# -----------------------
st.title("DD Hospital Chatbot")

st.subheader("Chat with bot")
msg = st.text_input("Type your message:")

if st.button("Send"):
    try:
        response = requests.post("http://127.0.0.1:8000/chat", json={"message": msg})
        st.write(response.json()["reply"])
    except:
        st.write("Error connecting to chatbot. Make sure FastAPI server is running.")

st.markdown("---")
st.subheader("Book an Appointment")
name = st.text_input("Your Name")
date = st.date_input("Appointment Date")
time = st.text_input("Time (e.g., 10:00 AM)")

if st.button("Book Appointment"):
    try:
        response = requests.post("http://127.0.0.1:8000/appointment", json={
            "patient_name": name,
            "date": str(date),
            "time": time
        })
        st.success(response.json()["message"])
    except:
        st.error("Error booking appointment. Make sure FastAPI server is running.")
