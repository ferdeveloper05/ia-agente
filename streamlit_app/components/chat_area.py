import streamlit as st
import time
from utils.session import update_conversation_title

def simulate_ai_response(prompt):
    """Simulates an AI backend response."""
    time.sleep(1) # simulate thinking
    return f"Esta es una respuesta simulada a tu mensaje: '{prompt}'. Más adelante se conectará con el LLM."

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
                response = simulate_ai_response(prompt)
                st.markdown(response)
                
            current_conv["messages"].append({"role": "assistant", "content": response})
        
        # Force a rerun to update the sidebar if title changed
        if len(current_conv["messages"]) == 2:
            st.rerun()
