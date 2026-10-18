# agent.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from csv_create_vector import vector_store, embeddings
load_dotenv()

llm = ChatGoogleGenerativeAI(
    google_api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini-3.1-flash-lite",
    temperature=1
)

print("Connected to Gemini")

vector_store.load_local(
    folder_path="./vectorsdb",
    embeddings=embeddings,
    allow_dangerous_deserialization=True
)

print("Local Vector database loaded")

while True:
    user_input = input("Ask me about the CSV: ")

    if user_input.lower() == "exit":
        print("Agent : Bye Bye")
        exit(0)

    docs = vector_store.similarity_search(user_input, k=2)

    context = "\n".join(doc.page_content for doc in docs)

    response = llm.invoke(f"""
    - Context: {context}
    - Question: {user_input}
    - Please answer in plain text.
    - Do not use Markdown.
    - Do not use *, **, -, #, or bullet points.
    - List each item on a separate line.
    - Apart from that, if anything is asked, reply: I don't know.
    """)

    print("Agent Reply :", response.content[0]["text"])