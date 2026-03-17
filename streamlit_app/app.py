import streamlit as st
import pymongo
import os

# App configuration
st.set_page_config(
    page_title="AI Agent Dashboard",
    page_icon="🤖",
    layout="wide"
)

# Custom minimal styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# MongoDB Connection Structure
# MongoDB container is named 'agent_mongodb_container'
MONGO_URI = os.getenv("MONGO_URI", "mongodb://agent_mongodb_container:27017")
DB_NAME = "agente_inteligente_database"

@st.cache_resource
def init_connection():
    try:
        # Give a small timeout since this runs fast on start
        client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # Force a call to check if DB actually connects
        client.admin.command('ping')
        return client
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e}")
        return None

client = init_connection()

st.title("🤖 Intelligent Agent Dashboard")
st.markdown("### Overview and Architecture Integration")

col1, col2 = st.columns(2)

with col1:
    st.info("📊 **Streamlit Framework connected!**\n\nThe UI container 'intelligent_agent_dashboard' is running and actively rendering this workspace.")

with col2:
    if client:
        db = client[DB_NAME]
        st.success(f"✅ **MongoDB connected!**\n\nDatabase `{DB_NAME}` is structured and available from the 'agent_mongodb_container'. No documents have been populated yet.")
    else:
        st.warning("⏳ **Waiting for MongoDB connection...**\n\nEnsure 'agent_mongodb_container' is successfully running in Docker.")

st.markdown("---")
st.markdown("### Future Collections (Placeholders)")
st.write("This section will later display data retrieved by our Python AI agent backend from the MongoDB database.")
