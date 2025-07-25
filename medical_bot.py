import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Streamlit UI
st.set_page_config(page_title="🩺 Medical Chatbot", layout="centered")
st.title("🩺 Free Medical Chatbot (OpenRouter + DeepSeek)")

st.markdown("> ⚠️ This bot gives general health information. Always consult a real doctor for diagnosis.")

user_query = st.text_input("Ask a medical question")

# Call OpenRouter API
def get_medical_response(query):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": [
            {"role": "system", "content": "You are a helpful medical assistant. Do not provide diagnosis. Only provide general information."},
            {"role": "user", "content": query}
        ]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

# Show answer
if user_query:
    with st.spinner("Thinking..."):
        reply = get_medical_response(user_query)
        st.markdown(f"**💬 Chatbot:** {reply}")
# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Display chat history
for i, (user, bot) in enumerate(st.session_state.history):
    st.markdown(f"**You:** {user}")
    st.markdown(f"**Bot:** {bot}")

# Update API call to include past messages
def get_medical_response(query):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    messages = [{"role": "system", "content": "You are a medical assistant. Provide general info only."}]
    for user, bot in st.session_state.history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": bot})
    messages.append({"role": "user", "content": query})

    data = {"model": "deepseek/deepseek-chat-v3-0324:free", "messages": messages}
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

# Chat handling
if user_query:
    with st.spinner("Thinking..."):
        reply = get_medical_response(user_query)
        st.session_state.history.append((user_query, reply))
        st.rerun()
