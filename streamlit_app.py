# streamlit_app.py

import streamlit as st

# -----------------------
# FAQ / simple chatbot
# -----------------------
FAQ = {
    "fever": "Please take rest and drink fluids.",
    "headache": "Take some rest and stay hydrated.",
    "appointment": "You can book an appointment anytime.",
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
