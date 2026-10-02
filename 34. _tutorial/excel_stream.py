# python -m streamlit run excel_stream.py
import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import chromadb
load_dotenv()
# Gemini
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
# ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="excel_documents")
# Streamlit UI
st.title("Excel RAG Agent")
user_input = st.text_input(
    "Ask report about retail sales"
)
if st.button("Submit"):
    if user_input:
        # Create query embedding
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=user_input
        )
        query_embedding = response.embeddings[0].values
        # Search ChromaDB
        result = collection.query(
            query_embeddings=[query_embedding],
            n_results=1
        )
        # Get Excel data
        context = "\n".join(
            result["documents"][0]
        )
        # Ask Gemini
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=f"""
            Context: {context}
            Question: {user_input}
            -Please use the above context to answer.
            -If the answer is not present in the context, say "I don't know".
        """)
        st.write("### Agent Final Reply")
        st.write(response.text)