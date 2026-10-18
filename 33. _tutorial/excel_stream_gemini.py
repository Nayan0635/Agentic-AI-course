import os
import streamlit as st

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from excel_create_vector import vector_store, embeddings

load_dotenv()

llm = ChatGoogleGenerativeAI(
    google_api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini-3.1-flash-lite",
    temperature=1
)

vector_store.load_local(
    folder_path="./excel_vectorsdb",
    embeddings=embeddings,
    allow_dangerous_deserialization=True
)

st.title("Retail Sales RAG")

with st.form("question_form"):
    user_input = st.text_input("Ask me about Retail Sales")
    submit = st.form_submit_button("Submit")

if submit and user_input:

    docs = vector_store.similarity_search(
        user_input,
        k=2
    )

    context = "\n".join(
        doc.page_content for doc in docs
    )

    response = llm.invoke(f"""
    - Context:
    {context}

    - Question:
    {user_input}

    - Please use the above context to reply.
    - Apart from that, if anything is asked, reply:
      I don't know.
    """)

    st.write("### Agent Reply")
    st.write(response.content[0]["text"])


# python -m streamlit run excel_stream_gemini.py