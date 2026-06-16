# Day 5-6 - Optimize & Testing

## Muc tieu

Toi uu pipeline co ban va viet test de dam bao chatbot khong hong khi sua code.

## 1. Embedding Cache

### Dinh nghia

Embedding cache luu lai embedding da tinh. Neu chunk khong doi, khong can tinh embedding lai.

### Vi du key

```text
cache_key = hash(chunk_text)
```

## 2. Batch Processing

### Dinh nghia

Batch processing xu ly nhieu chunks cung luc. Khi goi embedding API that, batch giup nhanh va tiet kiem request.

### Vi du concept

```python
embeddings = embedding_model.embed_documents(chunks)
```

## 3. Pytest

### Dinh nghia

Pytest la testing framework cho Python. Test giup kiem tra function co output dung.

### Vi du

```python
def test_chunk_text():
    chunks = chunk_text("hello world", chunk_size=5, overlap=0)
    assert chunks
```

## 4. Unit Test RAG

### Dinh nghia

Unit test RAG service kiem tra retrieval va answer generation voi data nho, khong can server.

### Vi du expectation

```text
Question: Which week teaches OCR?
Expected source: week2:c1
```

## 5. Error Case Test

### Dinh nghia

Error case test dam bao app tra loi dung khi chua upload file, question rong, file rong.

### Vi du

```python
def test_ask_without_chunks_returns_unknown():
    answer = service.ask("anything")
    assert "do not know" in answer["answer"].lower()
```

## Bai tap

Viet tests:

- Test chunking.
- Test retrieve dung source.
- Test answer co citations.
- Test question rong.

## Checklist

- Hieu embedding cache.
- Hieu batch processing.
- Viet duoc pytest unit test.
- Test duoc RAG service khong can UI.
- Biet test error case.

