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
collection = chroma_client.get_or_create_collection(name="excel_documents")
print("Collection loaded")
# Chat Loop
while True:
    user_input = input("Ask about sales reports: ")
    if user_input.strip().lower() == "exit":
        print("Agent: Bye Bye")
        break
    if not user_input.strip():
        continue
    # Create query embedding
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=user_input
    )
    query_embedding = response.embeddings[0].values
    # Search ChromaDB
    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=4
    )
    # Get relevant Excel data
    documents = result.get("documents") or [[]]
    context = "\n".join(documents[0]) if documents and documents[0] else "No relevant context found."
    # print("\nRAG Context:", context)
    # Ask Gemini
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=f"""
            Context: {context}
            Question: {user_input}
            -Please use the above context to answer.
            -If the answer is not present in the context, say "I don't know".
        """)
    print("\nAgent Final Reply:")
    print(response.text)