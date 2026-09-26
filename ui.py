import os

import requests
import streamlit as st

API_URL = os.getenv("RAG_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Document Q&A", page_icon="📚", layout="wide")
st.title("📚 Document Q&A")
st.caption("Upload documents, then ask grounded questions with source citations.")

with st.sidebar:
    st.header("Documents")
    upload = st.file_uploader("Upload a PDF, DOCX, TXT, MD, or CSV", type=["pdf", "docx", "txt", "md", "csv"])
    if upload and st.button("Index document", use_container_width=True):
        with st.spinner("Extracting text and creating embeddings…"):
            response = requests.post(f"{API_URL}/documents", files={"file": (upload.name, upload.getvalue(), upload.type)}, timeout=180)
        if response.ok:
            st.success(f"Indexed {response.json()['document']['chunks']} chunks.")
            st.rerun()
        else:
            st.error(response.json().get("detail", "Upload failed"))
    try:
        documents = requests.get(f"{API_URL}/documents", timeout=10).json()
        for document in documents:
            col, delete_col = st.columns([5, 1])
            col.caption(f"{document['filename']} · {document['chunks']} chunks")
            if delete_col.button("×", key=document["id"], help="Delete document"):
                requests.delete(f"{API_URL}/documents/{document['id']}", timeout=30)
                st.rerun()
    except requests.RequestException:
        st.warning("API is not running. Start it with `uvicorn app.api:app --reload`.")

if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        for source in message.get("sources", []):
            with st.expander(f"{source['filename']}" + (f" · page {source['page']}" if source["page"] else "")):
                st.caption(source["excerpt"])

question = st.chat_input("Ask a question about your documents")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Searching documents…"):
            try:
                response = requests.post(f"{API_URL}/ask", json={"question": question}, timeout=120)
                response.raise_for_status()
                result = response.json()
                st.markdown(result["answer"])
                for source in result["sources"]:
                    with st.expander(f"{source['filename']}" + (f" · page {source['page']}" if source["page"] else "")):
                        st.caption(source["excerpt"])
                st.session_state.messages.append({"role": "assistant", "content": result["answer"], "sources": result["sources"]})
            except requests.RequestException as exc:
                st.error(f"Could not answer: {exc}")
