# Bnk Chatbot

Local company knowledge chatbot for BNK internal documents: company info, rules, regulations, policies, procedures, benefits, HR notes, and related files.

Architecture follows root `README.md`:

```text
Chat UI/Admin UI (Streamlit) -> API Gateway (FastAPI)
Document upload -> Text Extract/OCR stage -> Query Engine (RAGService)
Query Engine -> Vector DB (ChromaDB)
Query Engine -> LLM (Gemini)
LLM -> Query Engine -> API Gateway -> Chat UI
```

## Pages

- `Chatbot`: ask questions. If company context exists, answer uses document citations. If no company context and question is outside company scope, Gemini answers normally.
- `Admin`: upload, review, approve, replace, re-index, and delete documents.

## Document Policy

- Company-related document: status `approved`, chunks indexed into ChromaDB.
- Weak or unrelated document: status `needs_review`, file is stored but not indexed.
- Admin can click `Approve & Index` to index a `needs_review` document.

Supported upload types:

```text
.txt, .md, .csv, .pdf, .docx, .xlsx, .xlsm
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Gemini Config

Create `.env` from `.env.example`:

```powershell
Copy-Item .env.example .env
```

Then set a new Gemini key:

```env
GEMINI_API_KEY=your_new_gemini_key_here
GEMINI_MODEL=gemini-3.5-flash
GEMINI_TIMEOUT_SECONDS=10
```

Do not commit `.env`. It is ignored by git.

## Run Backend

```powershell
uvicorn backend.main:app --host 127.0.0.1 --port 8002 --reload
```

Open:

```text
http://127.0.0.1:8002/docs
```

## Run Frontend

```powershell
streamlit run frontend/app.py
```

If backend runs on another port:

```powershell
$env:API_BASE_URL="http://127.0.0.1:8002"
streamlit run frontend/app.py
```

Open:

```text
http://127.0.0.1:8501
```

## Data Files

```text
data/documents.json      # document registry and status
data/chunks.json         # approved chunks used by RAG
data/chat_sessions.json  # persistent chat sessions and messages
data/uploads/            # original uploaded files
data/chroma_db/          # ChromaDB vector database
data/conversations.json  # chat history
```

## Run Tests

```powershell
python -m unittest discover -s tests
```
