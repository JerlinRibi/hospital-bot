# app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# -----------------------
# FastAPI App
# -----------------------
app = FastAPI(
    title="DD Hospital Chatbot",
    description="Simple hospital chatbot with appointment booking and symptom-based replies",
    version="1.0"
)

# -----------------------
# Enable CORS
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # allow all methods
    allow_headers=["*"]   # allow all headers
)

# -----------------------
# Pydantic Model
# -----------------------
class ChatRequest(BaseModel):
    message: str

# -----------------------
# FAQ / chatbot logic
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
@app.get("/hello")
def hello():
    return {"message": "Welcome to DD Hospital"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(request: ChatRequest):
    text = request.message.lower()
    reply = "Sorry, I didn’t understand. Please ask about appointments, doctors, or hospital info."
    for key in FAQ:
        if key in text:
            reply = FAQ[key]
            break
    return {"reply": reply}

# -----------------------
# Optional: Run locally
# -----------------------
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
