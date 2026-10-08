import streamlit as st
from core.rag import answer

st.title("📚 RAG Chatbot")
user_input = st.text_input("Ask a question about your documents")

if st.button("Submit") and user_input:
    with st.spinner("Thinking..."):
        st.write("### Agent Final Reply")
        st.write(answer(user_input))


# import streamlit as st
# from core.rag import answer

# st.title("RAG Chatbot")
# q = st.text_input("Ask a question")
# if st.button("Submit") and q:
#     with st.spinner("Thinking..."):
#         st.write("### Agent Final Reply")
#         st.write(answer(q))