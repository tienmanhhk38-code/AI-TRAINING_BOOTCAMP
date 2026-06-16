# Day 3 - Embeddings & Vector DB

## Muc tieu

Hieu embeddings, vector DB va cosine similarity de tim context lien quan.

## 1. Embedding

### Dinh nghia

Embedding la vector so bieu dien y nghia cua text. Text giong nhau ve nghia thi vector gan nhau.

### Vi du

```text
"OCR extracts text" -> [0.12, 0.87, 0.33, ...]
"OCR reads images"  -> [0.10, 0.83, 0.35, ...]
```

## 2. Vector DB

### Dinh nghia

Vector DB luu embeddings va metadata. No cho phep search vector gan nhat voi query.

### Vi du metadata

```python
{
    "chunk_id": "week2:c1",
    "source": "week2",
    "text": "Week 2 focuses on OCR.",
    "embedding": [0.1, 0.2, 0.3]
}
```

## 3. Cosine Similarity

### Dinh nghia

Cosine similarity do do giong nhau giua 2 vector. Gia tri cang cao thi text cang lien quan.

### Vi du code

```python
import math

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0

    return dot / (norm_a * norm_b)
```

## 4. ChromaDB / FAISS

### Dinh nghia

ChromaDB va FAISS la cong cu luu/search vector. ChromaDB de dung cho app local. FAISS nhanh va phu hop search vector lon.

### Vi du concept

```text
chunks -> embeddings -> add to vector DB
question -> query embedding -> search top-k chunks
```

## 5. Simple Local Embedding

### Dinh nghia

Trong project hoc, co the dung bag-of-words embedding de hieu logic truoc khi dung model embedding that.

### Vi du

```python
from collections import Counter

def embed_text(text):
    words = text.lower().split()
    return Counter(words)
```

## Bai tap

Tao file:

```text
day3_embeddings.py
```

Yeu cau:

- Tao 3 chunks text.
- Tao query.
- Embed bang bag-of-words.
- Tinh cosine similarity.
- In top 2 chunks lien quan nhat.

## Checklist

- Giai thich duoc embedding la gi.
- Hieu vector DB luu gi.
- Tinh duoc cosine similarity.
- Biet top-k retrieval la gi.
- Biet ChromaDB/FAISS dung de lam gi.

