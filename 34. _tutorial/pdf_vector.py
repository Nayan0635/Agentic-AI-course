from google import genai
from dotenv import load_dotenv
import os
import chromadb
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
pdf_file = "./documents/ejob.pdf"
reader = PdfReader(pdf_file)
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_text(text)
# if not chunks:
#     raise ValueError("The PDF contains no extractable text; no chunks were created.")

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="pdf_documents")

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=chunks
)
embeddings = [item.values for item in response.embeddings]
source = "data.pdf"
collection.add(
    ids=[f"pdf_{i}" for i in range(len(chunks))],
    embeddings=embeddings,
    documents=chunks,
    # metadatas=[{"source": source, "chunk_index": i} for i in range(len(chunks))]
)
print("PDF chunks stored")
