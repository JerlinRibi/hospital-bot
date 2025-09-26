from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

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
# Endpoints
# -----------------------

# 1️⃣ Hello endpoint
@app.get("/hello")
def read_hello():
    return {"message": "Welcome to DD Hospital"}

# 2️⃣ Appointment endpoint
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

# 3️⃣ Chatbot endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    text = request.message.lower()
    reply = "Sorry, I didn’t understand. Please ask about appointments, doctors, or hospital info."
    for key in FAQ:
        if key in text:
            reply = FAQ[key]
            break

    # Save chat log to DB
    db = SessionLocal()
    chat_log = ChatLogDB(message=request.message, reply=reply)
    db.add(chat_log)
    db.commit()
    db.close()

    return {"reply": reply}

# 4️⃣ View all appointments (Admin)
@app.get("/appointments")
def get_appointments():
    db = SessionLocal()
    appointments = db.query(AppointmentDB).all()
    db.close()
    return appointments

# 5️⃣ View all chat logs (Admin)
@app.get("/chatlogs")
def get_chatlogs():
    db = SessionLocal()
    logs = db.query(ChatLogDB).all()
    db.close()
    return logs
