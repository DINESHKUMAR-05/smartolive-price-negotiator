import streamlit as st
import requests
import uuid

st.set_page_config(page_title="SmartOlive Price Negotiator", page_icon="🤖", layout="wide")
st.title("SmartOlive AI Price Negotiator")

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'thread_id' not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

def send_message(message):
    url = "http://localhost:8000/negotiate/"
    payload = {
        "customer_input": message,
        "thread_id": st.session_state.thread_id
    }
    response = requests.post(url, json=payload)
    return response.json()['agent_response']

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Chat with our AI Price Negotiator"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = send_message(prompt)
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

st.sidebar.title("SmartOlive Products")
st.sidebar.markdown("""
### AI Driven Vacuum Cleaner
- Price: $800
- Power Intake: 100 watts
- Charging time: 30 minutes
- Usage: 4 hours/charge
- Weight: 3.5 kg with charger

### AI Driven Air Conditioner
- Price: $1000
- Power Intake: 900 watts
- Coverage: 100 sq feet
- Load: 1.5 ton
- Weight: 40 kg

### AI Driven Washing Machine
- Price: $1100
- Power Intake: 800 watts
- Weight: 60 kg

All products come with a 2-year warranty.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("Contact Us:")
st.sidebar.markdown("Email: sales@smartolive.com")
st.sidebar.markdown("Phone: +91 9876543210")
st.sidebar.markdown("Website: www.smartolive.com")
