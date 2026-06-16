# Day 7 - Cloud OCR & Chunking

## Muc tieu

Hieu khi nao dung Cloud OCR va biet clean/chunk text dau ra cho pipeline RAG.

## 1. Cloud OCR

### Dinh nghia

Cloud OCR la dich vu OCR chay tren cloud, vi du Google Vision API. No thuong tot hon OCR local voi anh phuc tap, nhieu ngon ngu, layout kho.

### Vi du use case

```text
Input: invoice scan chat luong thap
Cloud OCR output: text + bounding boxes + confidence
```

## 2. Local OCR vs Cloud OCR

| Tieu chi | Local OCR | Cloud OCR |
| --- | --- | --- |
| Chi phi | Re hon khi chay nhieu local | Co phi theo usage |
| Setup | Can cai engine/model | Can API key |
| Bao mat | Du lieu o local | Gui file len cloud |
| Chat luong | Tot voi file don gian | Tot hon voi layout kho |
| Toc do | Phu thuoc may local | Phu thuoc network/service |

## 3. Cloud OCR pseudo-code

### Dinh nghia

Pseudo-code la code mo ta y tuong, chua can chay that vi can credential/API key.

### Vi du

```python
def call_cloud_ocr(image_path, api_key):
    # 1. Read image bytes
    # 2. Send request to OCR provider
    # 3. Parse text annotations
    # 4. Return extracted text
    return "extracted text"
```

## 4. Text Cleaning

### Dinh nghia

Text cleaning la chuan hoa raw OCR text: xoa dong trong, giam space thua, sua ky tu thua, gom line.

### Vi du

```python
import re

def clean_text(text):
    text = text.replace("\r\n", "\n")
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    text = "\n".join(lines)
    text = re.sub(r"[ \t]+", " ", text)
    return text
```

## 5. Chunking

### Dinh nghia

Chunking la chia text dai thanh doan nho. RAG can chunk de index vao Vector DB va retrieve dung context.

### Vi du

```python
def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

        if start < 0:
            start = 0

    return chunks
```

## 6. Metadata

### Dinh nghia

Metadata la thong tin di kem chunk, giup citation va filtering.

### Vi du chunk object

```python
{
    "chunk_id": "sample.pdf:p1:c1",
    "source": "sample.pdf",
    "page": 1,
    "text": "Invoice No: INV-001..."
}
```

## Bai tap

Tao file:

```text
day7_chunking.py
```

Yeu cau:

- Doc `output/extracted_text.txt`.
- Clean text.
- Chunk text voi `chunk_size=500`, `overlap=50`.
- Moi chunk co `chunk_id`, `source`, `text`.
- Ghi ra `output/chunks.json`.

## Checklist

- Biet khi nao dung Cloud OCR.
- Hieu trade-off local OCR vs Cloud OCR.
- Clean duoc raw OCR text.
- Chunk duoc text.
- Them metadata cho chunk.

