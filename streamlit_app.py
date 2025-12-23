import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/query"

st.set_page_config(
    page_title="RAG ChatBot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 RAG ChatBot")
st.caption("Ask questions across all documents. Chat remembers context.")

# ---------------- SESSION MEMORY ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- USER INPUT ----------------
user_input = st.chat_input("Ask your question...")

if user_input:
    # Add user message to memory
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Build conversational context (last N messages)
    conversation_context = ""
    for msg in st.session_state.chat_history[-6:]:
        conversation_context += f"{msg['role']}: {msg['content']}\n"

    with st.spinner("Thinking..."):
        response = requests.post(
            API_URL,
            params={
                "question": conversation_context
            },
            timeout=120
        )

        if response.status_code == 200:
            answer = response.json()["answer"]

            st.session_state.chat_history.append(
                {"role": "assistant", "content": answer}
            )

            with st.chat_message("assistant"):
                st.markdown(answer)
        else:
            error_msg = "Backend error occurred."
            st.session_state.chat_history.append(
                {"role": "assistant", "content": error_msg}
            )
            with st.chat_message("assistant"):
                st.error(error_msg)
