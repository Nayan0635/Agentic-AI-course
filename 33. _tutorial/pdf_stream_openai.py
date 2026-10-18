import streamlit as st
from langchain_openai import ChatOpenAI
# from langchain_community.vectorstores.faiss import FAISS
from dotenv import load_dotenv
import os
from pdf_create_vector import vector_store, embeddings
load_dotenv()
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4.1-mini",
    temperature=1
)
vector_store.load_local(
    folder_path="./vectorsdb",
    embeddings=embeddings,
    allow_dangerous_deserialization=True
)
st.title("PDF RAG OPENAI")
user_input = st.text_input("Ask me about EjobIndia")
if st.button("Ask"):
    if user_input:
        # Retrieve relevant documents
        docs = vector_store.similarity_search(
            user_input,
            k=2
        )
        # Create RAG context
        context = "\n".join(
            doc.page_content for doc in docs
        )
        # Send context + question to LLM
        response = llm.invoke(f"""
        -Context: {context}
        -Question: {user_input}
        -Please use the above context to reply.
        Apart from that if anything asked reply: "I don't know".
        """)
        # Display response
        st.write("### Agent Reply")
        st.write(response.content)
    else:
        st.warning("Please enter a question.")