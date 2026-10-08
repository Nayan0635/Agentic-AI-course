from core import embedder, llm
from core.vector_store import collection


def answer(question: str, n_results: int = 3) -> str:
    q_emb = embedder.embed(question)

    result = collection.query(
        query_embeddings=[q_emb],
        n_results=n_results,
    )
    context = "\n\n---\n\n".join(result["documents"][0])

    return llm.ask(context, question)



# from core import embedder, vector_store, llm

# def answer(question: str, n_results: int = 2) -> str:
#     q_emb = embedder.embed(question)
#     context = vector_store.query(q_emb, n=n_results)
#     return llm.ask(context, question)