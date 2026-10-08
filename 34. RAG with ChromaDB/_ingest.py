import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

from loaders import load_file
from core import embedder
from core.vector_store import collection        # ← import the collection object


def ingest(path: str):
    print(f"Loading {path} ...")
    text = load_file(path)
    print(f"   Extracted {len(text)} characters.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    print(f"   Splited into {len(chunks)} chunks.")

    print("   Embedding chunks ...")
    embeddings = [embedder.embed(chunk) for chunk in chunks]

    source = os.path.basename(path)
    ids       = [f"{source}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": source, "chunk_index": i} for i in range(len(chunks))]  #-->need

    # delete old chunks of this source, then upsert new ones — DIRECT calls
    collection.delete(where={"source": source})
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )

    print(f"✅ Stored {len(chunks)} chunks from '{source}' in chromaDB")


if __name__ == "__main__":
    path = input("Enter file_path (e.g. documents/file.txt): ").strip()
    if path:
        ingest(path)
    else:
        print("❌ No path given. Exiting.")



# documents/data.txt
# documents/mission_Titan.pdf
# documents/retail_sales.xlsx
# documents/space_missions.csv
# documents/urban_gardening.docx

