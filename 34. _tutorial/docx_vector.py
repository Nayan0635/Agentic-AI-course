from google import genai
from dotenv import load_dotenv
import os
import chromadb
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()
# Gemini
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
# Read DOCX
doc = Document("./documents/urban_gardening.docx")
text = "\n".join(
    paragraph.text
    for paragraph in doc.paragraphs
    if paragraph.text.strip()
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_text(text)
if not chunks:
    raise ValueError("The DOCX file contains no text; no chunks were created.")
# ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="docx_documents")
# Create Embedding
response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=chunks
)
embeddings = [item.values for item in response.embeddings]
collection.delete(where={"source": "urban_gardening.docx"})
collection.upsert(
    ids=[f"docx_{i}" for i in range(len(chunks))],
    embeddings=embeddings,
    documents=chunks,
    # metadatas=[{"source": source, "chunk_index": i} for i in range(len(chunks))]
)
print("DOCX chunks stored successfully")