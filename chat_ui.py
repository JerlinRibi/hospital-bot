import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="DD Hospital Chatbot", page_icon="🏥")
st.title("🏥 DD Hospital Chatbot")

# ----------------- Sidebar -----------------
st.sidebar.title("Navigation")
option = st.sidebar.selectbox(
    "Go to",
    ["Chatbot", "Book Appointment", "View Appointments", "View Chat Logs"]
)

# ----------------- In-Memory Database -----------------
# Using lists instead of SQLite for Streamlit Cloud
appointments = []
chatlogs = []

# ----------------- FAQ -----------------
FAQ = {
    "fever": "Please take rest and drink fluids.",
    "headache": "Take some rest and stay hydrated.",
    "appointment": "You can book an appointment here!",
    "doctor": "Our doctors are available Mon-Fri, 9AM-5PM.",
    "working hours": "Our hospital is open Mon-Fri 9AM-5PM.",
    "hospital info": "DD Hospital is located at Main Street.",
    "emergency": "For emergency, call 108 immediately.",
    "insurance": "We accept most major insurance providers."
}

# ----------------- Chatbot -----------------
if option == "Chatbot":
    st.subheader("Chat with Bot")
    msg = st.text_input("Type your message:")
    if st.button("Send"):
        if msg.strip() != "":
            reply = "Sorry, I didn’t understand. Please ask about appointments, doctors, or hospital info."
            for key in FAQ:
                if key in msg.lower():
                    reply = FAQ[key]
                    break
            st.write(reply)
            # Save to chat logs
            chatlogs.append({"message": msg, "reply": reply, "created_at": str(datetime.datetime.now())})

# ----------------- Book Appointment -----------------
elif option == "Book Appointment":
    st.subheader("Book an Appointment")
    with st.form("appointment_form"):
        name = st.text_input("Your Name")
        date = st.date_input("Select Date")
        time = st.text_input("Select Time (e.g., 10:00 AM)")
        submitted = st.form_submit_button("Book Appointment")
        if submitted:
            if name.strip() == "" or time.strip() == "":
                st.error("Please enter all fields")
            else:
                appointment = {
                    "patient_name": name,
                    "date": str(date),
                    "time": time,
                    "created_at": str(datetime.datetime.now())
                }
                appointments.append(appointment)
                st.success(f"Appointment booked for {name} on {date} at {time}")

# ----------------- View Appointments -----------------
elif option == "View Appoint
