from openai import OpenAI
from dotenv import load_dotenv
import os
import chromadb

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
#Connect to ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="company_documents")
# print("Collection loaded")

#ChatLoop
while True:
    user_input = input("Ask About Ejobindia only: ")
    if user_input.strip().lower() == "exit":
        print("Agent : Bye Bye")

    responses = client.embeddings.create(
        model="text-embedding-3-small",
        input=user_input
    )
    query_embedding = responses.data[0].embedding
    # Search ChromaDB for the most relevant chunks.
    result=collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )
    #Get the relavant documents
    context = "\n".join(result['documents'][0])
    # print("Rag Context :",context)
    #Now sending this context to llm
    responses= client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"user","content":f'''
              -Context :{context}
              -Question:{user_input}
              -Please use above context to answer , otherwise say I dont know
            '''}
        ]
    )
    '''add a system prompt — better grounding & role clarity.'''
    msg = responses.choices[0].message.content
    print("Agent Final Reply :",msg)
    
