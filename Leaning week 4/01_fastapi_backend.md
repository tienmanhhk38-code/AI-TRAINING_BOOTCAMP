# Day 1-2 - FastAPI Backend

## Muc tieu

Xay backend local co API upload file va hoi dap RAG.

## 1. FastAPI

### Dinh nghia

FastAPI la framework Python de xay HTTP API nhanh, co validation va OpenAPI docs tu dong.

### Vi du

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```

## 2. Endpoint

### Dinh nghia

Endpoint la URL ma client goi vao backend. Moi endpoint nen co input/output ro rang.

### Vi du endpoint can co

| Method | Path | Muc dich |
| --- | --- | --- |
| GET | `/health` | Kiem tra backend song |
| POST | `/upload` | Upload file va index chunks |
| POST | `/ask` | Gui question va nhan answer |

## 3. Request/Response

### Dinh nghia

Request la du lieu client gui len. Response la du lieu backend tra ve.

### Vi du ask request

```json
{
  "question": "Week 4 build what?"
}
```

### Vi du ask response

```json
{
  "answer": "Week 4 builds a local AI Chatbot.",
  "sources": ["week4:c1"]
}
```

## 4. Chay server

```powershell
uvicorn backend.main:app --reload
```

## Bai tap

Tao FastAPI app co:

- `GET /health`
- `POST /ask`
- Response JSON co `answer`, `sources`
- Doc Gemini key tu `.env`, khong hardcode key trong code

## Checklist

- Hieu FastAPI dung de lam gi.
- Tao duoc endpoint.
- Biet request/response la gi.
- Chay duoc backend local.
- Mo duoc `/docs`.
- Biet cach fallback local khi chua co Gemini key.
