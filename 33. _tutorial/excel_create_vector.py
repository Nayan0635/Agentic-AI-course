import os
import pandas as pd

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

# Read Excel file
df = pd.read_excel("./assets/retail_sales.xlsx")

# Convert Excel data to text
excel_data = df.to_string(index=False)

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

documents = text_splitter.split_text(excel_data)

# Create Gemini embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Create vector store
vector_store = FAISS.from_texts(
    documents,
    embeddings
)

# Save vector database
vector_store.save_local("./excel_vectorsdb")

print("Excel Vector Database created successfully")