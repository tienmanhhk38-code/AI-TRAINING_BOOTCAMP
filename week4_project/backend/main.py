import os
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from backend.chat_store import ChatSessionStore
from backend.chroma_store import ChromaStore
from backend.document_loader import DocumentLoadError, SUPPORTED_EXTENSIONS, load_document_text
from backend.document_policy import classify_document
from backend.document_store import DocumentStore, build_document_record, save_uploaded_file
from backend.gemini_client import GeminiClient
from backend.rag_service import RAGService
from backend.storage import append_conversation, read_json, write_json

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
CHUNKS_PATH = DATA_DIR / "chunks.json"
DOCUMENTS_PATH = DATA_DIR / "documents.json"
CONVERSATIONS_PATH = DATA_DIR / "conversations.json"
CHAT_SESSIONS_PATH = DATA_DIR / "chat_sessions.json"
CHROMA_PATH = DATA_DIR / "chroma_db"

class AskRequest(BaseModel):
    question: str
    session_id: str | None = None

class ChatSessionCreateRequest(BaseModel):
    title: str = "New chat"

def load_env_file(path):
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())

def status_counts(documents):
    counts = {}
    for document in documents:
        status = document.get("status", "unknown")
        counts[status] = counts.get(status, 0) + 1
    return counts

def current_date_text():
    return datetime.now().astimezone().strftime("%A, %B %d, %Y")

def persist_chunks():
    write_json(CHUNKS_PATH, rag_service.chunks)

def extract_saved_document(document):
    saved_path = Path(document["saved_path"])
    if not saved_path.exists():
        raise HTTPException(status_code=404, detail="Saved file not found")
    try:
        text = load_document_text(document["filename"], saved_path.read_bytes())
    except DocumentLoadError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    if not text:
        raise HTTPException(status_code=400, detail="Document has no extractable text")
    return text

def index_document(document, text):
    chunks = rag_service.replace_document(
        text,
        source=document["filename"],
        document_id=document["id"],
    )
    persist_chunks()
    return document_store.update(
        document["id"],
        status="approved",
        chunk_count=len(chunks),
        text_preview=text[:300],
    )

app = FastAPI(title="Bnk Chatbot")
load_env_file(PROJECT_DIR / ".env")
gemini_client = GeminiClient.from_env()
try:
    vector_store = ChromaStore(CHROMA_PATH)
except Exception:
    vector_store = None

document_store = DocumentStore(DOCUMENTS_PATH)
chat_session_store = ChatSessionStore(CHAT_SESSIONS_PATH)
rag_service = RAGService(
    read_json(CHUNKS_PATH, []),
    llm_client=gemini_client,
    vector_store=vector_store,
)

@app.get("/health")
def health():
    documents = document_store.list()
    return {
        "status": "ok",
        "app": "Bnk Chatbot",
        "chunk_count": len(rag_service.chunks),
        "document_count": len(documents),
        "chat_session_count": len(chat_session_store.list_summaries()),
        "document_statuses": status_counts(documents),
        "supported_extensions": sorted(SUPPORTED_EXTENSIONS),
        "llm": "gemini" if rag_service.llm_client else "local",
        "llm_model": rag_service.llm_client.model if rag_service.llm_client else "local",
        "vector_db": "chroma" if rag_service.vector_store else "local",
    }

@app.get("/chat/sessions")
def list_chat_sessions():
    return chat_session_store.list_summaries()

@app.post("/chat/sessions")
def create_chat_session(payload: ChatSessionCreateRequest):
    return chat_session_store.create(payload.title)

@app.get("/chat/sessions/{session_id}")
def get_chat_session(session_id: str):
    session = chat_session_store.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return session

@app.post("/chat/sessions/{session_id}/clear")
def clear_chat_session(session_id: str):
    session = chat_session_store.clear(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return session

@app.delete("/chat/sessions/{session_id}")
def delete_chat_session(session_id: str):
    deleted = chat_session_store.delete(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return {"deleted": session_id}

@app.get("/documents")
def list_documents():
    return document_store.list()

@app.get("/documents/{document_id}")
def get_document(document_id: str):
    document = document_store.get(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    try:
        text = load_document_text(file.filename, content)
    except DocumentLoadError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    if not text:
        raise HTTPException(status_code=400, detail="Document has no extractable text")

    policy = classify_document(file.filename, text)
    saved_path = save_uploaded_file(UPLOAD_DIR, file.filename, content)
    document = build_document_record(
        filename=file.filename,
        saved_path=saved_path,
        file_size=len(content),
        status=policy["status"],
        policy=policy,
        text=text,
    )
    document_store.add(document)

    if document["status"] == "approved":
        document = index_document(document, text)

    return {
        "document": document,
        "total_chunks": len(rag_service.chunks),
    }

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return await upload_document(file)

@app.post("/documents/{document_id}/replace")
async def replace_document(document_id: str, file: UploadFile = File(...)):
    document = document_store.get(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    try:
        text = load_document_text(file.filename, content)
    except DocumentLoadError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    if not text:
        raise HTTPException(status_code=400, detail="Document has no extractable text")

    old_path = Path(document.get("saved_path", ""))
    saved_path = save_uploaded_file(UPLOAD_DIR, file.filename, content)
    policy = classify_document(file.filename, text)

    rag_service.remove_document(document_id)
    persist_chunks()
    if old_path.is_file():
        old_path.unlink()

    updated = document_store.update(
        document_id,
        filename=file.filename,
        saved_path=str(saved_path),
        file_size=len(content),
        status=policy["status"],
        policy_score=policy["score"],
        policy_reason=policy["reason"],
        matched_keywords=policy["matched_keywords"],
        chunk_count=0,
        text_preview=text[:300],
    )

    if updated["status"] == "approved":
        updated = index_document(updated, text)

    return {
        "document": updated,
        "total_chunks": len(rag_service.chunks),
    }

@app.post("/documents/{document_id}/approve")
def approve_document(document_id: str):
    document = document_store.get(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    text = extract_saved_document(document)
    updated = index_document(document, text)
    return {
        "document": updated,
        "total_chunks": len(rag_service.chunks),
    }

@app.post("/documents/{document_id}/reindex")
def reindex_document(document_id: str):
    document = document_store.get(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    text = extract_saved_document(document)
    updated = index_document(document, text)
    return {
        "document": updated,
        "total_chunks": len(rag_service.chunks),
    }

@app.delete("/documents/{document_id}")
def delete_document(document_id: str):
    document = document_store.get(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    rag_service.remove_document(document_id)
    persist_chunks()
    document_store.delete(document_id)

    saved_path = Path(document.get("saved_path", ""))
    if saved_path.is_file():
        saved_path.unlink()

    return {
        "deleted": document_id,
        "total_chunks": len(rag_service.chunks),
    }

@app.post("/ask")
def ask(payload: AskRequest):
    current_session = chat_session_store.get(payload.session_id) if payload.session_id else None
    history = current_session.get("messages", []) if current_session else []
    answer_record = rag_service.ask(
        payload.question,
        history=history,
        current_date=current_date_text(),
    )
    append_conversation(CONVERSATIONS_PATH, payload.question, answer_record)
    session = chat_session_store.add_exchange(
        payload.session_id,
        payload.question,
        answer_record,
    )
    answer_record["session_id"] = session["id"]
    answer_record["session_title"] = session["title"]
    return answer_record
