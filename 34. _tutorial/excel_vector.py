import pandas as pd
from google import genai
from dotenv import load_dotenv
import os
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()
# Gemini
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
# print("Gemini connected")
# Read Excel
excel_file = "./documents/retail_sales.xlsx"
df = pd.read_excel(excel_file)
excel_data = df.to_string(index=False)
# print("Excel loaded")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_text(excel_data)
if not chunks:
    raise ValueError("The Excel file contains no data; no chunks were created.")
# ChromaDB
chroma_client = chromadb.PersistentClient(path="./chromaDB")
collection = chroma_client.get_or_create_collection(name="excel_documents")
# Create Embedding
response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=chunks
)
embeddings = [item.values for item in response.embeddings]
collection.delete(where={"source": "retail_sales.xlsx"})
collection.upsert(
    ids=[f"excel_{i}" for i in range(len(chunks))],
    embeddings=embeddings,
    documents=chunks,
    # metadatas=[{"source": source, "chunk_index": i} for i in range(len(chunks))]
)
print("Excel chunks stored successfully")