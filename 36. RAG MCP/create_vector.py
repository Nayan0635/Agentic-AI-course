from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

import os


load_dotenv()
all_documents=[] #empty list
##We will be reading a pdf.
reader = PdfReader("./documents/EjobIndia.pdf")
pdf_text="" #str
for page in reader.pages:
    pdf_text+=page.extract_text()
# print(pdf_text)

all_documents.append(pdf_text)

#Create the embeddings
embeddings = OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="text-embedding-3-small"
)
text_splitters = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
#Chunks creation.
documents=[]
for doc in all_documents:
    chunk=text_splitters.split_text(doc)
    documents.extend(chunk)

vector_store = FAISS.from_texts(
    documents,
    embeddings
)
#Store locally
vector_store.save_local(folder_path="./vectorstore")
# print("Local Vector Database is created successfully")
