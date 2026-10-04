# python -m streamlit run txt_stream.py
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import chromadb
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="company_documents")
st.title("TXT RAG OpenAI")
user_input = st.text_input("Ask about EjobIndia")
if st.button("Ask"):
    if user_input:
        # Create query embedding
        responses = client.embeddings.create(
            model="text-embedding-3-small",
            input=user_input
        )
        query_embedding = responses.data[0].embedding
        # Search ChromaDB
        result = collection.query(
            query_embeddings=[query_embedding],
            n_results=2
        )
        # Get relevant documents
        context = "\n".join(result["documents"][0])
        # Send context to LLM
        responses = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                        Context: {context}
                        Question: {user_input}
                    -Please use the above context to answer.
                    -Otherwise say "I don't know".
                    """
                }
            ]
        )
        msg = responses.choices[0].message.content
        st.write("### Agent Final Reply")
        st.write(msg)