import chromadb
import config

_client = chromadb.PersistentClient(path=config.CHROMA_PATH)
collection = _client.get_or_create_collection(name=config.COLLECTION_NAME)





# import chromadb
# import config

# _client = chromadb.PersistentClient(path=config.CHROMA_PATH)

# def get_collection():
#     return _client.get_or_create_collection(name=config.COLLECTION_NAME)

# def add(doc_id: str, embedding: list[float], text: str):
#     get_collection().add(ids=[doc_id], embeddings=[embedding], documents=[text])

# def query(embedding: list[float], n: int = 2) -> str:
#     result = get_collection().query(query_embeddings=[embedding], n_results=n)
#     return "\n".join(result["documents"][0])