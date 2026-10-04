'''marking errors'''
from openai import OpenAI
from dotenv import load_dotenv
import os
import chromadb #importing chromadb vector database

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
# print("OpenAI connected")

#Create Chromadb vector database
chroma_client = chromadb.PersistentClient(path="./chroma_db")
#Create a collection where we need to store the vector data.
collection = chroma_client.get_or_create_collection(name="company_documents")

text=""
#fetching from .txt file 
'''remove "r+" (write mode not needed, can corrupt file). Use "r" only.'''
with open("./documents/ejob.txt","r+") as file: 
    text = file.read()
    file.close()
    '''remove file.close() — "with" already handles closing automatically.'''
print(text)

#Create the embeddings 
responses = client.embeddings.create(
    model="text-embedding-3-small",
    input=text
)
embedding = responses.data[0].embedding
# print(embedding)
#We need to store these vectors inside the collection of the chromadb.
collection.add(
    ids=['doc1'],
    embeddings=[embedding],
    documents=[text]
    
)
'''the whole file content was read into
a single variable `text` and then passed directly into
`client.embeddings.create(input=text)`.

Result:
- Only ONE embedding was generated for the entire document.
- The whole document became a single vector.
- This is bad RAG practice because retrieval can only return the
entire document as one match — no granularity, no relevance.
- If the file grows large, it can even exceed the embedding model's
token limit (text-embedding-3-small = 8191 tokens).
'''
print("ChromaDB created successfully")
'''fix for other files too'''