from app.rag.loader import load_markdown
from app.rag.splitter import split_text


content = load_markdown(
    "app/rag/turning.md"
)

chunks = split_text(
    content,
    chunk_size=200,
    overlap=50,
)

print(f"原始文本长度: {len(content)}")
print(f"Chunk 数量: {len(chunks)}")

for index, chunk in enumerate(chunks):

    print("\n" + "=" * 50)

    print(f"Chunk {index + 1}")

    print("=" * 50)

    print(chunk)