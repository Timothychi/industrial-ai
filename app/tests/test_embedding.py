from app.rag.embedding import EmbeddingModel


model = EmbeddingModel()

texts = [
    "45号钢是什么材料？",
    "45号钢属于什么钢材？",
    "铝合金有哪些特点？",
]

for text in texts:

    vector = model.embed(text)

    print("文本:", text)
    print("向量维度:", len(vector))
    print("前10个值:", vector[:10])
    print()