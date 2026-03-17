import streamlit as st
from components.sidebar import sidebar_custom
from components.chat_area import chat_container

from utils.session import init_session_state

# We must instantiate session state early enough or before rendering so theme is ready
init_session_state()

# App configuration
st.set_page_config(
    page_title="Mi Chatbot AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom dark mode overrides
custom_css = """
<style>
    .stChatInputContainer { padding-bottom: 2rem; }
    /* Dark mode manual overrides if config.toml base="dark" isn't enough */
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    [data-testid="stSidebar"] { background-color: #1E293B; }
    div[data-testid="stSidebarNav"] li a:hover { background-color: #334155; }
    h1, h2, h3, p { color: #FAFAFA !important; }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Main Application Layout
sidebar_custom()
chat_container()
