import streamlit as st
import uuid

def init_session_state():
    """Initializes the session state variables required for the chat."""
    if "conversations" not in st.session_state:
        st.session_state.conversations = {}
        
        # Create the first conversation
        first_id = str(uuid.uuid4())
        st.session_state.conversations[first_id] = {
            'title': 'Nueva conversación',
            'messages': []
        }
        st.session_state.current_conversation_id = first_id

    if "current_conversation_id" not in st.session_state or st.session_state.current_conversation_id not in st.session_state.conversations:
        if st.session_state.conversations:
            st.session_state.current_conversation_id = list(st.session_state.conversations.keys())[0]
        else:
            create_new_conversation()

def switch_conversation(conv_id):
    """Switches the active conversation."""
    st.session_state.current_conversation_id = conv_id

def create_new_conversation():
    """Creates a new, empty conversation and sets it as active."""
    new_id = str(uuid.uuid4())
    st.session_state.conversations[new_id] = {
        'title': 'Nueva conversación', 
        'messages': []
    }
    st.session_state.current_conversation_id = new_id
    st.rerun()

def delete_conversation(conv_id):
    """Deletes a conversation by its ID."""
    if conv_id in st.session_state.conversations:
        del st.session_state.conversations[conv_id]
        
    # If we deleted the currently active conversation, switch to another one
    if st.session_state.current_conversation_id == conv_id:
        if st.session_state.conversations:
            st.session_state.current_conversation_id = list(st.session_state.conversations.keys())[0]
        else:
            # If no conversations left, create a new one
            create_new_conversation()
    st.rerun()
    
def update_conversation_title():
    """Updates the conversation title based on the first user message."""
    if st.session_state.current_conversation_id in st.session_state.conversations:
        current_conv = st.session_state.conversations[st.session_state.current_conversation_id]
        if current_conv['messages']:
            first_msg = current_conv['messages'][0]['content']
            # Take the first 20 characters as title
            title = first_msg[:20] + "..." if len(first_msg) > 20 else first_msg
            current_conv['title'] = title
