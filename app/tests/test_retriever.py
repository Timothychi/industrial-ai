from app.rag.retriever import Retriever


retriever = Retriever()

query = "45号钢车削需要注意什么？"

results = retriever.search(
    query,
    top_k=5,
)

print("查询:", query)

for index, result in enumerate(results):

    print("\n" + "=" * 60)

    print(
        f"结果 {index + 1}"
    )

    print(
        "向量分数:",
        result["vector_score"]
    )

    print(
        "Rerank 分数:",
        result["rerank_score"]
    )

    print(
        "材料:",
        result["material"]
    )

    print(
        "工艺:",
        result["process"]
    )

    print(
        "章节:",
        result["section"]
    )

    print(
        "内容:"
    )

    print(
        result["text"]
    )