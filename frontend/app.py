import streamlit as st
import requests
import uuid
import os

# URL of API to pass user question
API_URL = os.getenv('API_URL', 'http://backend:8000/query').rstrip('/')

# Title of project
st.title("MathBot")

# Session state for chat history, session_id
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())



# Display Q&A pairs by matching 'user' and 'assistant' roles
messages = st.session_state["messages"]
pair = []
for msg in messages:
    if msg["role"] == "user":
        pair = [msg]
    elif msg["role"] == "assistant" and pair:
        pair.append(msg)
        # Display user then assistant
        st.markdown(f'<div style="text-align:right;background:#DCF8C6;padding:8px;border-radius:10px;margin:4px 0;">{pair[0]["content"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align:left;background:#F1F0F0;padding:8px;border-radius:10px;margin:4px 0;">{pair[1]["content"]}</div>', unsafe_allow_html=True)
        st.markdown("<hr style='margin: 12px 0;'>", unsafe_allow_html=True)
        pair = []
# If last message is a user message without a response
if pair and pair[0]["role"] == "user":
    st.markdown(f'<div style="text-align:right;background:#DCF8C6;padding:8px;border-radius:10px;margin:4px 0;">{pair[0]["content"]}</div>', unsafe_allow_html=True)

# User input
if prompt := st.chat_input("Ask Math question or type Ping..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.markdown(f'<div style="text-align:right;background:#DCF8C6;padding:8px;border-radius:10px;margin:4px 0;">{prompt}</div>', unsafe_allow_html=True)

    # Call backend API
    payload = {
        "question": prompt
    }
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        response.raise_for_status()
        ai_message = response.json().get("response", "")
    except Exception as e:
        ai_message = f"[Error contacting backend: {e}]"

    # Append Response to session, such that it can be displayed in frontend
    st.session_state["messages"].append({"role": "assistant", "content": ai_message})
    st.markdown(f'<div style="text-align:left;background:#F1F0F0;padding:8px;border-radius:10px;margin:4px 0;">{ai_message}</div>', unsafe_allow_html=True)

