# Week 3 Project - Local RAG Chatbot

## Muc tieu

Xay RAG chatbot local co the tra loi cau hoi tu chunks va dua ra citations.

## 1. Input

### Dinh nghia

Input la danh sach chunks tu Week 2. Moi chunk co text va metadata.

### Vi du

```json
{
  "chunk_id": "week2:c1",
  "source": "week2",
  "text": "Week 2 focuses on OCR."
}
```

## 2. Output

### Dinh nghia

Output la danh sach answers gom question, answer, sources, scores.

### Vi du

```json
{
  "question": "Week 2 hoc gi?",
  "answer": "Week 2 focuses on OCR.",
  "sources": ["week2:c1"]
}
```

## 3. Module

| File | Trach nhiem |
| --- | --- |
| `main.py` | Dieu phoi RAG flow |
| `embeddings.py` | Tokenize, embed, cosine similarity |
| `vector_store.py` | Index chunks va search top-k |
| `retriever.py` | Lay context lien quan |
| `generator.py` | Tao answer tu context |
| `evaluator.py` | Danh gia answer co context/source |

## 4. Flow

```text
chunks.json
  -> build vector store
  -> embed question
  -> retrieve top-k chunks
  -> generate answer from context
  -> evaluate
  -> answers.json
```

## 5. Acceptance checklist

- Chay bang mot lenh: `python src/main.py`.
- Doc chunks tu `input/chunks.json`.
- Search duoc top-k context.
- Answer co source/citation.
- Ghi `output/answers.json`.
- Khong can API key de chay local.

## 6. Mo rong sau bai hoc

- Doi local embedding thanh Gemini embedding.
- Doi in-memory vector store thanh ChromaDB/FAISS.
- Doi local generator thanh Gemini/Groq LLM.
- Them LangChain chain.
- Them RAGAS evaluation.

