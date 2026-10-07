from app.rag.loader import load_markdown
from app.rag.splitter import split_markdown
from app.rag.splitter import enrich_metadata

content = load_markdown(
    "app/rag/turning.md"
)

chunks = split_markdown(
    content,
    source="turning.md",
)

for chunk in chunks:
    print(chunk)
    enrich_metadata(chunk)
    print(chunk)