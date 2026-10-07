from sentence_transformers import CrossEncoder


class CrossEncoderReranker:

    def __init__(self):

        self.model = CrossEncoder(
            "BAAI/bge-reranker-base"
        )

    def rerank(
        self,
        query: str,
        documents: list[dict],
        top_k: int = 5,
    ) -> list[dict]:

        pairs = [
            [query, document["text"]]
            for document in documents
        ]

        scores = self.model.predict(pairs)

        results = []

        for document, score in zip(
            documents,
            scores,
        ):
            item = dict(document)

            item["rerank_score"] = float(score)

            results.append(item)

        results.sort(
            key=lambda x: x["rerank_score"],
            reverse=True,
        )

        return results[:top_k]