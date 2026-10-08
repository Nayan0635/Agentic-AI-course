import pandas as pd
from google import genai
from dotenv import load_dotenv
import os
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

csv_file = "./documents/space_missions.csv"
df = pd.read_csv(csv_file)
csv_data = df.to_string(index=False)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_text(csv_data)
# if not chunks:
#     raise ValueError("The CSV file contains no data; no chunks were created.")
chroma_client = chromadb.PersistentClient(path="./chromaDB")
collection = chroma_client.get_or_create_collection(name="csv_documents")

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=chunks
)
embeddings = [item.values for item in response.embeddings]
collection.delete(where={"source": "space_missions.csv"})
collection.upsert(
    ids=[f"csv_{i}" for i in range(len(chunks))],
    embeddings=embeddings,
    documents=chunks,
    # metadatas=[{"source": source, "chunk_index": i} for i in range(len(chunks))]
)
print("CSV chunks stored")