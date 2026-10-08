'''run this file once()'''
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores.faiss import FAISS
from embeddings import embeddings

'''extract pdf content'''

reader = PdfReader("./documents/mission_Titan.pdf")
text : str ="" #where we are going to dump all contents from pdf.
for page in reader.pages:
    text+=page.extract_text()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_text(text) # becomes list of strings
# print(chunks)
'''create vector embedding'''

vector_store = FAISS.from_texts(chunks, embeddings) #embedding complete
# print(vector_store)
vector_store.save_local(folder_path = "./faissDB")
print("Vector Embedding succefully created.")