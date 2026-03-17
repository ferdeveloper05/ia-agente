import streamlit as st
from PIL import Image
from utils.session import (
    init_session_state,
    create_new_conversation,
    switch_conversation,
    delete_conversation
)

@st.dialog("Conectar Correo Electrónico")
def email_connection_modal():
    st.write("Ingresa los datos para conectar tu correo electrónico.")
    email = st.text_input("Correo Electrónico", placeholder="ejemplo@correo.com")
    password = st.text_input("Contraseña / App Password", type="password")
    
    if st.button("Conectar", type="primary"):
        st.success(f"Correo {email} conectado (Simulado)!")
        # Más adelante conectaremos esto a la BD
        # st.rerun()

def sidebar_custom():
    init_session_state()
    
    # Logo
    try:
        logo = Image.open('assets/logos/deepseek-color1.png')
        st.logo(image=logo, size='large')
    except FileNotFoundError:
        pass # Optional warning if logo is not found
        
    with st.sidebar:
        st.title("🤖 Chatbot AI")
        
        # New chat button
        if st.button('➕ Nueva conversación', use_container_width=True, type='primary'):
            create_new_conversation()
            
        st.divider()
        st.subheader("Historial")
        
        # List conversations
        sorted_convs = sorted(
            st.session_state.conversations.items(),  
            reverse=True
        )
        
        for conv_id, conv_data in sorted_convs:
            is_active = conv_id == st.session_state.current_conversation_id
            
            # Layout for title and delete button
            col1, col2 = st.columns([0.8, 0.2])
            
            with col1:
                button_type = 'secondary' if is_active else 'tertiary'
                if st.button(
                    f"💬 {conv_data['title']}", 
                    key=f"conv_{conv_id}",
                    use_container_width=True,
                    type=button_type
                ):
                    switch_conversation(conv_id)
            
            with col2:
                if st.button("🗑️", key=f"del_{conv_id}"):
                    delete_conversation(conv_id)
        
        st.divider()
        
        # Connect Email Button
        if st.button("📧 Conectar Correo", use_container_width=True):
            email_connection_modal()
