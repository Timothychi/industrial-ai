from app.rag.loader import load_markdown
from app.rag.splitter import split_markdown
from app.rag.embedding import EmbeddingModel
from app.rag.vector_store import MilvusStore
from app.rag.splitter import enrich_metadata
import sys


def main():

    content = load_markdown(
        "app/rag/turning.md"
    )

    chunks = split_markdown(
        content,
        "turning.md",
        chunk_size=500,
        overlap=100,
    )

    embedding_model = EmbeddingModel()

    vectors = []

    for chunk in chunks:
        chunk = enrich_metadata(chunk)

        vector = embedding_model.embed(
            chunk["text"]
        )

        vectors.append(vector)

    dimension = len(vectors[0])

    store = MilvusStore()

    # 删除collection
    store.drop_collection()

    # 创建collection
    store.create_collection(
        dimension=dimension
    )

    data = []

    for chunk, vector in zip(
        chunks,
        vectors,
    ):

        data.append(
            {
                "vector": vector,
                "text": chunk["text"],
                "source": chunk["source"],
                "title": chunk["title"],
                "section": chunk["section"],
                "material": chunk["material"],
                "process": chunk["process"],
            }
        )

    result = store.insert(data)

    print("知识入库完成")

    print(result)


if __name__ == "__main__":
    main()