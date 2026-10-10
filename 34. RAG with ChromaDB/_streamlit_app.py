import streamlit as st
from core.rag import answer

st.title("📚 RAG Chatbot")
user_input = st.text_input("Ask a question about your documents")

if st.button("Submit") and user_input:
    with st.spinner("Thinking..."):
        st.write("### Agent ")
        st.write(answer(user_input))
