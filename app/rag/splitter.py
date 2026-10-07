import re


def split_markdown(
    text: str,
    source: str,
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[dict]:

    chunks = []

    current_title = ""
    current_section = ""

    paragraphs = re.split(r"\n\s*\n", text)

    buffer = ""

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        # 一级标题
        if paragraph.startswith("# "):
            current_title = paragraph[2:].strip()
            continue

        # 二级标题
        if paragraph.startswith("## "):
            current_section = paragraph[3:].strip()
            continue

        if len(buffer) + len(paragraph) > chunk_size:

            if buffer:
                chunks.append(
                    {
                        "text": buffer,
                        "source": source,
                        "title": current_title,
                        "section": current_section,
                    }
                )

            # 保留一部分上下文
            buffer = buffer[-overlap:] + "\n" + paragraph

        else:

            if buffer:
                buffer += "\n\n"

            buffer += paragraph

    if buffer:
        chunks.append(
            {
                "text": buffer,
                "source": source,
                "title": current_title,
                "section": current_section,
            }
        )

    return chunks

def enrich_metadata(chunk: dict) -> dict:

    text = chunk["text"]

    material = None
    process = None

    if "45号钢" in text:
        material = "45号钢"

    elif "铝合金" in text:
        material = "铝合金"

    if "车削" in text:
        process = "车削"

    elif "铣削" in text:
        process = "铣削"

    chunk["material"] = material
    chunk["process"] = process

    return chunk