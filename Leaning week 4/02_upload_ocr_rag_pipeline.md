# Day 1-2 - Upload, OCR, RAG Pipeline

## Muc tieu

Ket noi upload file voi pipeline extract text, chunk, index, retrieve, answer.

## 1. Upload File

### Dinh nghia

Upload file la buoc nguoi dung gui document len backend. Backend luu file tam hoac doc noi dung ngay.

### Vi du FastAPI

```python
from fastapi import UploadFile

async def read_upload(file: UploadFile):
    content = await file.read()
    return content.decode("utf-8")
```

## 2. OCR/Text Extract

### Dinh nghia

OCR/Text Extract la buoc lay text tu file. File text doc truc tiep. PDF/image can pipeline Week 2.

### Vi du

```text
sample.txt -> read text
sample.pdf -> extract text or render image -> OCR
sample.png -> OCR
```

## 3. RAG Index

### Dinh nghia

RAG index la buoc clean text, chunk text, embed chunks va luu vao vector store.

### Flow

```text
uploaded text -> clean -> chunk -> embed -> store
```

## 4. Async Processing

### Dinh nghia

Async processing giup backend khong bi block khi xu ly file lau. Week 4 ban co ban co the xu ly sync, sau do mo rong sang background task.

### Vi du concept

```python
from fastapi import BackgroundTasks

def process_file(path):
    pass

@app.post("/upload")
def upload(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_file, "file.txt")
```

## 5. Error Handling

### Dinh nghia

Error handling giup API tra loi loi ro rang khi file sai format, text rong, RAG chua co index.

### Vi du loi

```json
{
  "detail": "No indexed document. Upload a file first."
}
```

## Bai tap

Tao endpoint `/upload`:

- Nhan file `.txt`.
- Doc text.
- Chunk text.
- Index chunks vao RAG service.
- Tra ve `chunk_count`.

## Checklist

- Upload duoc file.
- Extract duoc text.
- Chunk va index duoc.
- Tra loi loi ro rang.
- Hieu sync vs async processing.

