# Week 4 - Build & Demo AI Chatbot

Nguon lo trinh: `../README.md`

Muc tieu Week 4: demo Bnk Chatbot chay local cho hoi dap tai lieu noi bo cong ty.

Flow can nam:

```text
Admin Upload -> Needs Review/Approve -> OCR/Text Extract -> Chunk -> ChromaDB Vector DB -> Chatbot Q&A -> Gemini/Local Answer + Citations
```

## Danh sach bai hoc

| Ngay | File | Noi dung |
| --- | --- | --- |
| Day 1-2 | [01_fastapi_backend.md](01_fastapi_backend.md) | FastAPI backend, endpoint, request/response |
| Day 1-2 | [02_upload_ocr_rag_pipeline.md](02_upload_ocr_rag_pipeline.md) | Upload file, OCR/RAG pipeline, async/error handling |
| Day 3-4 | [03_streamlit_chat_ui.md](03_streamlit_chat_ui.md) | Streamlit chat UI, citations, conversation history |
| Day 5-6 | [04_optimization_testing.md](04_optimization_testing.md) | Embedding cache, batch processing, pytest |
| Day 7 | [05_local_demo_project.md](05_local_demo_project.md) | Local demo checklist va video walkthrough |

## Cach hoc moi ngay

1. Doc dinh nghia.
2. Chay vi du nho.
3. Ket noi backend/frontend.
4. Test flow end-to-end.
5. Tick checklist.

## Deliverable cuoi tuan

Project dau ra da tao o `../week4_project/`.

```text
week4_project/
  backend/
    chroma_store.py
    document_loader.py
    document_policy.py
    document_store.py
    gemini_client.py
    main.py
    rag_service.py
    storage.py
  frontend/
    app.py
  data/
    chroma_db/
    chunks.json
    conversations.json
    documents.json
    uploads/
  tests/
    test_rag_service.py
  requirements.txt
  README.md
```

Chay backend:

```powershell
cd ../week4_project
uvicorn backend.main:app --reload
```

Chay frontend:

```powershell
streamlit run frontend/app.py
```

Tieu chi dat:

- Backend co endpoint health, documents, upload, approve, replace, reindex, delete, ask.
- Upload duoc `.txt`, `.md`, `.csv`, `.pdf`, `.docx`, `.xlsx`, `.xlsm`.
- Tai lieu khong ro lien quan cong ty vao status `needs_review`, chua index.
- Admin co the approve/reindex/delete tai lieu.
- Chunks duoc luu va search trong ChromaDB.
- Ask question va nhan answer + citations.
- Cau hoi ngoai cong ty va khong co context thi Gemini tra loi binh thuong.
- Neu co `GEMINI_API_KEY`, backend dung Gemini de generate answer.
- Neu chua co `GEMINI_API_KEY`, backend fallback local de van demo duoc.
- Streamlit UI co input chat va hien history.
- Co test cho RAG service.
- Co README huong dan demo local.
