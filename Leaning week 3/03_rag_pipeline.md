# Day 4-5 - RAG Pipeline

## Muc tieu

Hieu va lap duoc flow RAG: chunking, indexing, retrieval, generate answer.

## 1. RAG

### Dinh nghia

RAG la Retrieval-Augmented Generation. He thong tim context lien quan trong tai lieu truoc, sau do dua context vao LLM de tra loi.

### Flow

```text
Question -> Retrieve Context -> Prompt -> LLM -> Answer with citations
```

## 2. Chunking

### Dinh nghia

Chunking chia tai lieu dai thanh doan nho. Chunk qua dai thi kho retrieve dung. Chunk qua ngan thi mat ngu canh.

### Vi du

```python
chunk = {
    "chunk_id": "week2:c1",
    "source": "week2",
    "text": "Week 2 focuses on OCR pipeline."
}
```

## 3. Indexing

### Dinh nghia

Indexing la buoc embed chunks va luu vao vector store.

### Vi du

```text
for chunk in chunks:
    embedding = embed(chunk["text"])
    vector_store.add(chunk, embedding)
```

## 4. Retrieval

### Dinh nghia

Retrieval la tim top-k chunks lien quan nhat voi question.

### Vi du

```python
top_chunks = vector_store.search("Week 2 hoc gi?", top_k=3)
```

## 5. Generate Answer

### Dinh nghia

Generation la buoc tao cau tra loi tu question + retrieved context.

### Prompt template

```text
Use the context below to answer.
If context is insufficient, say you do not know.

Context:
{context}

Question:
{question}

Answer:
```

## 6. Citation

### Dinh nghia

Citation la nguon cua context duoc dung de tra loi. Chatbot tai lieu can citation de nguoi dung kiem chung.

### Vi du

```json
{
  "answer": "Week 2 focuses on OCR.",
  "sources": ["week2:c1"]
}
```

## Bai tap

Tao file:

```text
day4_rag_pipeline.py
```

Yeu cau:

- Load `chunks.json`.
- Embed chunks.
- Nhap question.
- Retrieve top 3 chunks.
- Build prompt.
- In answer gia lap dua tren context.

## Checklist

- Giai thich duoc RAG.
- Phan biet indexing va retrieval.
- Build duoc prompt co context.
- Tra loi co citation.
- Biet khi nao answer phai "khong biet".

