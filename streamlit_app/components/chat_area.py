import streamlit as st
import time
import requests
import os
from utils.session import update_conversation_title

# Configuration of API URL - Default to Docker service name if not provided
API_URL = os.getenv("API_URL", "http://app:8000/api/v1/ask")

def call_ai_backend(session_id, prompt):
    """Calls the FastAPI backend to get a response."""
    try:
        response = requests.post(
            API_URL,
            json={"session_id": session_id, "question": prompt},
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("response", "No se obtuvo respuesta del agente.")
        else:
            return f"Error ({response.status_code}): {response.text}"
    except Exception as e:
        return f"Error de conexión con el backend: {str(e)}"

def chat_container():
    if "current_conversation_id" not in st.session_state or st.session_state.current_conversation_id not in st.session_state.conversations:
        return
        
    st.title("🤖 Bienvenido a tu chatbot de IA Sirpef", )
    
    current_conv = st.session_state.conversations[st.session_state.current_conversation_id]
    
    # Render existing messages
    for message in current_conv['messages']:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
            
    # Chat Input
    if prompt := st.chat_input('Escribe tu mensaje...'):
        # Append user message
        current_conv['messages'].append({'role': 'user', 'content': prompt})
        
        # Update title if it's the first message
        if len(current_conv['messages']) == 1:
            update_conversation_title()
            
        with st.chat_message('user'):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Escribiendo..."):
                response = call_ai_backend(st.session_state.current_conversation_id, prompt)
                st.markdown(response)
                
            current_conv["messages"].append({"role": "assistant", "content": response})
        
        # Force a rerun to update the sidebar if title changed
        if len(current_conv["messages"]) == 2:
            st.rerun()
