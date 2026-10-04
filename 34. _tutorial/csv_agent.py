from google import genai
from dotenv import load_dotenv
import os
import chromadb
load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
print("Gemini connected")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="csv_documents")

print("Collection loaded")
while True:
    user_input = input("Ask about the space missions: ")
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
    # Get relevant documents
    documents = result.get("documents") or [[]]
    context = "\n".join(documents[0]) if documents and documents[0] else "No relevant context found."
    # print("\nRAG Context:")
    # print(context)
    # Gemini
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=f"""
            Context: {context}
            Question: {user_input}
            - Please answer in plain text.
            - Do not use Markdown.
            - Do not use *, **, -, #, or bullet points.
            - List each item on a separate line.
            - Apart from that, if anything is asked, reply: I don't know.
        """)
    print("\nAgent Final Reply:")
    print(response.text)