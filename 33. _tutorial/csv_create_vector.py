# create_vector.py for csv
import os
import pandas as pd
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

# Read CSV
df = pd.read_csv("./assets/space_missions.csv")
text = df.to_string(index=False)

# Split text
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

documents = text_splitter.split_text(text)

# Gemini Embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Create vector database
vector_store = FAISS.from_texts(
    documents,
    embeddings
)

# Save vector database
vector_store.save_local("./vectorsdb")

print("Local Vector Database created successfully")