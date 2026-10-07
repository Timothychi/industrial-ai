from app.rag.retriever import Retriever


retriever = Retriever()


def search_knowledge(query: str) -> dict:

    results = retriever.search(
        query=query,
        top_k=5,
    )

    if not results:
        return {
            "found": False,
            "query": query,
            "results": [],
        }

    return {
        "query": query,
        "results": results,
    }