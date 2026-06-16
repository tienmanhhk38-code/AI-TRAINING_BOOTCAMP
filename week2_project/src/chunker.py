import json
import re


def clean_text(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    text = "\n".join(lines)
    return re.sub(r"[ \t]+", " ", text)


def chunk_text(text, source, chunk_size=500, overlap=50):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap must be greater than or equal to 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    index = 1

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append({
                "chunk_id": f"{source}:c{index}",
                "source": source,
                "index": index,
                "text": chunk,
            })
            index += 1

        if end == len(text):
            break

        start = end - overlap

    return chunks


def export_chunks(chunks, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=2)
