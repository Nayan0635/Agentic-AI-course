import os
import pandas as pd
import streamlit as st

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS

load_dotenv()

df = pd.read_csv("./assets/space_missions.csv")
csv_data = df.to_string(index=False)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

documents = text_splitter.split_text(csv_data)

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


vector_store = FAISS.from_texts(
    documents,
    embeddings
)
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=1
)

st.title("CSV RAG Chatbot")

user_input = st.text_input("Ask me about the CSV")

if st.button("Submit"):
    if user_input:

        docs = vector_store.similarity_search(
            user_input,
            k=2
        )

        context = "\n".join(
            doc.page_content for doc in docs
        )

        response = llm.invoke(f"""
        - Context: {context}
        - Question: {user_input}
        - Please use the above context to reply.
        - Apart from that if anything is asked reply: I don't know.
        """)

        st.write("### Agent Reply")
        st.write(response.content[0]["text"])

    else:
        st.warning("Please enter a question.")

# python -m streamlit run csv_stream_gemini.py