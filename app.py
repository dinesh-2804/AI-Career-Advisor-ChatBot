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

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Lato', sans-serif;
    background-color: #faf7f2;
    color: #2c2416;
}

[data-testid="stHeader"] { background: transparent !important; }

/* ── Warm paper texture background ── */
[data-testid="stAppViewContainer"] {
    background-color: #faf7f2;
    background-image:
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 34px,
            rgba(180,150,100,.06) 34px,
            rgba(180,150,100,.06) 35px
        ),
        radial-gradient(ellipse 70% 50% at 15% 20%, rgba(210,140,80,.10) 0%, transparent 55%),
        radial-gradient(ellipse 50% 60% at 85% 75%, rgba(180,110,60,.08) 0%, transparent 50%);
}

/* ── Thin accent line at top ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #c0622a 0%, #e8935a 40%, #c0622a 70%, #8b3e1a 100%);
    z-index: 9999;
}

/* ── Main block ── */
[data-testid="stMain"] > div { position: relative; z-index: 2; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #f0ece4; }
::-webkit-scrollbar-thumb { background: #c9a882; border-radius: 99px; }

/* ── Chat bubbles base ── */
[data-testid="stChatMessage"] {
    border-radius: 4px;
    padding: 18px 24px;
    margin-bottom: 16px;
    font-size: 15px;
    line-height: 1.8;
    animation: slideIn .3s ease both;
    position: relative;
    border: none;
    box-shadow: 0 1px 3px rgba(100,70,30,.08), 0 4px 16px rgba(100,70,30,.04);
    transition: box-shadow .2s, transform .2s;
}

[data-testid="stChatMessage"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 3px 12px rgba(100,70,30,.12), 0 8px 28px rgba(100,70,30,.06);
}

@keyframes slideIn {
    from { opacity: 0; transform: translateX(-10px); }
    to   { opacity: 1; transform: translateX(0); }
}

/* User bubble — warm cream with terracotta left border */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),
[data-testid="stChatMessage-user"] {
    background: #fff9f2 !important;
    border-left: 4px solid #c0622a !important;
}

/* Assistant bubble — off-white with sage left border */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]),
[data-testid="stChatMessage-assistant"] {
    background: #f5f0e8 !important;
    border-left: 4px solid #7a9e7e !important;
}

/* ── Avatar styling ── */
[data-testid="stChatMessageAvatarUser"] img {
    border-radius: 4px !important;
    box-shadow: 0 0 0 2px #c0622a, 0 2px 8px rgba(192,98,42,.3);
}
[data-testid="stChatMessageAvatarAssistant"] img {
    border-radius: 4px !important;
    box-shadow: 0 0 0 2px #7a9e7e, 0 2px 8px rgba(122,158,126,.3);
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: #fff9f2 !important;
    border: 1.5px solid #d4b896 !important;
    border-radius: 4px !important;
    box-shadow: 0 2px 8px rgba(100,70,30,.06) !important;
    transition: border-color .2s, box-shadow .2s !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #c0622a !important;
    box-shadow: 0 0 0 3px rgba(192,98,42,.1), 0 2px 12px rgba(192,98,42,.08) !important;
}

[data-testid="stChatInput"] textarea {
    color: #2c2416 !important;
    font-family: 'Lato', sans-serif !important;
    font-size: 15px !important;
    background: transparent !important;
    caret-color: #c0622a !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(44,36,22,.4) !important;
    font-style: italic;
}

/* ── Send button ── */
[data-testid="stChatInputSubmitButton"] button {
    background: #c0622a !important;
    border-radius: 4px !important;
    border: none !important;
    box-shadow: 0 2px 8px rgba(192,98,42,.35) !important;
    transition: background .15s, transform .15s, box-shadow .15s !important;
}
[data-testid="stChatInputSubmitButton"] button:hover {
    background: #a8521f !important;
    transform: scale(1.05) !important;
    box-shadow: 0 4px 14px rgba(192,98,42,.45) !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, #d4b896 30%, #d4b896 70%, transparent) !important;
    margin: 20px 0 !important;
}

/* ── "Start New Conversation" button ── */
.stButton > button {
    width: 100%;
    background: transparent !important;
    color: #c0622a !important;
    border: 1.5px solid #c0622a !important;
    border-radius: 4px !important;
    padding: 10px 28px !important;
    font-family: 'Lato', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 1.2px !important;
    text-transform: uppercase !important;
    transition: all .2s !important;
}

.stButton > button:hover {
    background: #c0622a !important;
    color: #fff9f2 !important;
    box-shadow: 0 4px 18px rgba(192,98,42,.3) !important;
    transform: translateY(-1px) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: #c0622a !important; }

/* ── Error box ── */
[data-testid="stAlert"] {
    background: #fff0eb !important;
    border: 1px solid #f0a882 !important;
    border-left: 4px solid #c0622a !important;
    border-radius: 4px !important;
    color: #7a2e0a !important;
}

/* ── Markdown text ── */
[data-testid="stMarkdown"] p,
[data-testid="stMarkdown"] li,
[data-testid="stMarkdown"] span {
    color: #2c2416 !important;
    line-height: 1.8 !important;
}

[data-testid="stMarkdown"] a { color: #c0622a !important; text-decoration: underline !important; }

[data-testid="stMarkdown"] strong { color: #8b3e1a !important; font-weight: 700 !important; }

[data-testid="stMarkdown"] code {
    background: #f0e8d8 !important;
    color: #8b3e1a !important;
    border-radius: 3px !important;
    padding: 2px 6px !important;
    font-size: 13px !important;
    border: 1px solid #d4b896 !important;
}

/* ── Column layout ── */
[data-testid="column"] { display: flex; align-items: center; justify-content: center; }

</style>
""", unsafe_allow_html=True)

# ------------------ Initialize Session ------------------
MemoryManager.initialize_session()

# ------------------ Header ------------------
st.markdown("""
<div style='text-align:center; padding: 36px 0 12px;'>
  <div style='
    display: inline-block;
    border-top: 2px solid #2c2416;
    border-bottom: 2px solid #2c2416;
    padding: 16px 40px;
    margin-bottom: 8px;
  '>
    <p style='
      font-family: "Lato", sans-serif;
      font-size: 10px;
      font-weight: 700;
      letter-spacing: 4px;
      text-transform: uppercase;
      color: #c0622a;
      margin-bottom: 6px;
    '>Your personal</p>
    <h1 style='
      font-family: "Playfair Display", serif;
      font-size: 38px;
      font-weight: 700;
      color: #2c2416;
      letter-spacing: -0.5px;
      line-height: 1;
      margin: 0;
    '>AI Career Advisor <span style="font-style:italic; font-weight:400; color:#c0622a;">🎓</span></h1>
    <p style='
      font-family: "Lato", sans-serif;
      font-size: 12px;
      font-weight: 300;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: rgba(44,36,22,.5);
      margin-top: 8px;
    '>Guiding every step of your journey</p>
  </div>
</div>
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