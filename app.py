from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="DD Hospital Chatbot")

# Allow frontend to access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str

FAQ = {
    "fever": "Please take rest and drink fluids.",
    "headache": "Take some rest and stay hydrated.",
    "appointment": "You can book an appointment using /appointment endpoint.",
    "doctor": "Our doctors are available Mon-Fri, 9AM-5PM.",
}

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
