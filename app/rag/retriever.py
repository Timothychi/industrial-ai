from app.rag.embedding import EmbeddingModel
from app.rag.vector_store import MilvusStore
from app.rag.reranker import CrossEncoderReranker


class Retriever:

    MIN_RERANK_SCORE = 0.5

    def __init__(self):

        self.embedding = EmbeddingModel()

        self.store = MilvusStore()

        self.reranker = CrossEncoderReranker()

    def search(self,query: str,top_k: int = 5) -> list[dict]:

        # 1. 向量召回
        query_vector = self.embedding.embed(
            query
        )

        candidates = self.store.search(
            query_vector=query_vector,
            top_k=20,
        )

        # 2. 整理 Milvus 结果
        documents = []

        for result in candidates:

            entity = result["entity"]

            documents.append(
                {
                    "text": entity["text"],
                    "source": entity["source"],
                    "title": entity["title"],
                    "section": entity["section"],
                    "material": entity["material"],
                    "process": entity["process"],
                    "vector_score": result["distance"],
                }
            )

        # 3. Reranker 精排
        results = self.reranker.rerank(
            query=query,
            documents=documents,
            top_k=top_k,
        )

        # 利用rerank得分进行过滤
        results = [
            result
            for result in results
            if result["rerank_score"] >= self.MIN_RERANK_SCORE
        ]

        return results