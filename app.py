import streamlit as st
import requests
from dotenv import load_dotenv
import os
import time

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# --- Define your bot's personality ---
SYSTEM_PROMPT = """
You are My-AI — a friendly, witty, and knowledgeable assistant built by Dhinesh.
Always answer helpfully, keep responses concise, and add light humor where it fits.
"""

# --- Streamlit setup ---
st.set_page_config(page_title="My-AI Chatbot 💬", page_icon="🤖")
st.title("🤖 My-AI (Smart + Funny)")
st.caption("Custom personality + typing animation ⚡")

# --- Initialize chat memory ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Display previous messages ---
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)

# --- User input section ---
if user_input := st.chat_input("Type your message..."):
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # --- Combine history and personality into one user message ---
    # Gemini no longer supports 'system' role, so we include prompt in the first turn.
    context_text = SYSTEM_PROMPT + "\n\nUser: " + user_input
    for role, msg in st.session_state.chat_history[-5:]:  # last few turns for memory
        if role == "assistant":
            context_text += f"\nAssistant: {msg}"
        elif role == "user":
            context_text += f"\nUser: {msg}"

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": context_text}]}
        ]
    }

    headers = {"Content-Type": "application/json"}

    # --- Send to Gemini ---
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        ai_response = data["candidates"][0]["content"]["parts"][0]["text"]
    else:
        ai_response = f"⚠️ Error {response.status_code}: {response.text}"

    # --- Typing animation effect ---
    with st.chat_message("assistant"):
        placeholder = st.empty()
        typed = ""
        for char in ai_response:
            typed += char
            placeholder.markdown(typed)
            time.sleep(0.015)
        placeholder.markdown(typed)

    st.session_state.chat_history.append(("assistant", ai_response))

