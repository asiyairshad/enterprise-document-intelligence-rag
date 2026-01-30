import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Enterprise RAG", layout="wide")
st.title("📄 Chat with your Document")

# -------- Upload Section --------
uploaded_file = st.file_uploader("Upload a PDF")

if uploaded_file:
    files = {"file": uploaded_file}
    res = requests.post(f"{API_URL}/upload", files=files)

    if res.status_code == 200:
        session_id = res.json()["session_id"]
        st.session_state.session_id = session_id
        st.success("Document processed successfully")
    else:
        st.error(res.text)

# -------- Chat Section --------
question = st.text_input("Ask a question about your document")

if st.button("Ask"):
    if "session_id" not in st.session_state:
        st.warning("Please upload a document first.")
    else:
        res = requests.post(
            f"{API_URL}/query-user",
            params={
                "question": question,
                "session_id": st.session_state.session_id
            }
        )

        if res.status_code == 200:
            data = res.json()
            st.subheader("Answer")
            st.write(data["answer"])

            st.subheader("Sources")
            for s in data["sources"]:
                st.markdown(f"- {s}")
        else:
            st.error(res.text)
