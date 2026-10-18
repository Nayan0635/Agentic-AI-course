from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
#for creating vector we need to import the following lib.
from langchain_community.vectorstores.faiss import FAISS
import os
load_dotenv()
#------------Reading content from PDF File -----------#
reader = PdfReader("./assets/EjobIndia.pdf")
text:str ="" #where we are going to dump all contents from pdf.
for page in reader.pages:
    text+=page.extract_text()
#print(text)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  #Standard values
    chunk_overlap=50
)
#Create documents of list
documents = text_splitter.split_text(text)
#print(documents)
#Now creating embedding
embeddings = OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="text-embedding-3-small"
)
#Creating the vector 
vector_store =FAISS.from_texts(
    documents,
    embeddings
)
#We can see local vector database is created.
#print(vector_store)
#Now saving the vector database locally
vector_store.save_local(folder_path="./vectorsdb")
print("Local Vector Database created successfully")
