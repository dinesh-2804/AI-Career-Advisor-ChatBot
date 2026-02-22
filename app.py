import streamlit as st
from backend.chatbot import CareerChatbot
from backend.memory_manager import MemoryManager
from backend.logger import setup_logger

# ------------------ Setup Logger ------------------
logger = setup_logger()
logger.info("Application started.")

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="AI Career Advisor",
    page_icon="🎓",
    layout="centered"
)

# ------------------ Peaceful UI Styling ------------------
st.markdown("""
<style>

/* Full App Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f9fafb 0%, #e6f4ea 100%);
}

/* Remove default header background */
[data-testid="stHeader"] {
    background: transparent;
}

/* Chat bubble style */
[data-testid="stChatMessage"] {
    border-radius: 18px;
    padding: 14px;
    margin-bottom: 12px;
    font-size: 15px;
}

/* User bubble */
[data-testid="stChatMessage-user"] {
    background-color: #dbeafe;
}

/* Assistant bubble */
[data-testid="stChatMessage-assistant"] {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
}

</style>
""", unsafe_allow_html=True)

# ------------------ Initialize Session ------------------
MemoryManager.initialize_session()

# ------------------ Header ------------------
st.markdown("""
<h1 style='text-align:center; font-size:34px; font-weight:600; color:#334155;'>
🎓 AI Career Advisor
</h1>
""", unsafe_allow_html=True)

st.divider()

# ------------------ Initialize Chatbot ------------------
if "chatbot" not in st.session_state:
    st.session_state.chatbot = CareerChatbot()
    logger.info("Chatbot initialized.")

# ------------------ Avatar Paths ------------------
user_avatar = "assets/user.png"
bot_avatar = "assets/chatbot.png"

# ------------------ Display Chat History ------------------
for msg in MemoryManager.get_history():
    if msg["role"] == "user":
        with st.chat_message("user", avatar=user_avatar):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar=bot_avatar):
            st.markdown(msg["content"])

# ------------------ Chat Input ------------------
user_input = st.chat_input("Ask your career question...")

if user_input:
    try:
        logger.info(f"User input received: {user_input}")

        # Show user message
        with st.chat_message("user", avatar=user_avatar):
            st.markdown(user_input)

        # Generate assistant response
        with st.chat_message("assistant", avatar=bot_avatar):
            with st.spinner("Thinking peacefully..."):
                response = st.session_state.chatbot.get_response(user_input)

            st.markdown(response)

        logger.info("Response displayed successfully.")

    except Exception as e:
        logger.error(f"UI error occurred: {str(e)}")
        st.error("⚠️ Something went wrong. Please refresh the page.")

# ------------------ Clear Button ------------------
st.divider()

col1, col2, col3 = st.columns([1,1,1])
with col2:
    if st.button("Start New Conversation"):
        logger.info("Conversation cleared by user.")
        MemoryManager.clear()
        st.rerun()