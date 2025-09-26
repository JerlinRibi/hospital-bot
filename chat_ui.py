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

# ⚠️ For online deployment, use your deployed FastAPI URL instead of localhost
# Example: BASE_URL = "https://your-app-name.streamlit.app"
BASE_URL = "http://127.0.0.1:8000"

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
            if name.strip() == "" or time.strip() == "":
                st.warning("Please fill all fields")
            else:
                try:
                    payload = {"patient_name": name, "date": str(date), "time": time}
                    response = requests.post(f"{BASE_URL}/appointment", json=payload)
                    st.success(response.json()["message"])
                except:
                    st.error("Error booking appointment. Make sure FastAPI server is running.")

# ----------------- View Appointments -----------------
elif option == "View Appointments":
    st.subheader("All Appointments")
    try:
        response = requests.get(f"{BASE_URL}/appointments")
        data = response.json()
        if len(data) > 0:
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.info("No appointments found.")
    except:
        st.error("Error fetching appointments. Make sure FastAPI server is running.")

# ----------------- View Chat Logs -----------------
elif option == "View Chat Logs":
    st.subheader("Chat Logs")
    try:
        response = requests.get(f"{BASE_URL}/chatlogs")
        data = response.json()
        if len(data) > 0:
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.info("No chat logs found.")
    except:
        st.error("Error fetching chat logs. Make sure FastAPI server is running.")
