from langchain_openai import ChatOpenAI
from langchain_community.vectorstores.faiss import FAISS # no longer maintained change it
from dotenv import load_dotenv
import os
from embeddings import embeddings

load_dotenv()

llm = ChatOpenAI(
    api_key= os.getenv("OPENAI_API_KEY"),
    model = "gpt-4.1-mini",
    temperature = 0.3
)

vector_store = FAISS.load_local(
    "./faissDB",
    embeddings,
    allow_dangerous_deserialization=True
) # local vector db loaded

while True:
    user_input = input("Ask: ")
    if user_input.strip().lower() in ['exit', 'quit']:
        print("Agent: Cya!")
        break
    docs = vector_store.similarity_search(user_input, k=2)
    context = "\n".join(doc.page_content for doc in docs)
    
    responses = llm.invoke(f'''
        You are an assistant for EjobIndia. Answer ONLY using the context below.
        # Rules:
        1. If the user's message is a greeting or thanks, reply briefly and normally.
        2. If the user asks a question that the context answers, answer it using the context.
        3. If the user asks a question the context does NOT answer, reply: "I don't know."
        4. Do not invent questions. Do not generate lists unless the user asks for one.
        Context: {context}
        User: {user_input}
    ''')
    
    print("Agent : ", responses.content)
#hi I'm codex
