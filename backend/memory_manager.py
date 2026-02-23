import streamlit as st

class MemoryManager:

    @staticmethod
    def initialize_session():
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

    @staticmethod
    def add_message(role, content):
        st.session_state.chat_history.append({
            "role": role,
            "content": content
        })

    @staticmethod
    def get_history():
        return st.session_state.chat_history

    @staticmethod
    def clear():
        st.session_state.chat_history = []