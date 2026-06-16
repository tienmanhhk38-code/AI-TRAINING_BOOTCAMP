from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from backend.storage import read_json, write_json

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def safe_filename(filename):
    name = Path(filename).name.strip() or "document"
    return "".join(char if char.isalnum() or char in "._- " else "_" for char in name)

def build_document_record(filename, saved_path, file_size, status, policy, text, chunk_count=0):
    now = utc_now()
    document_id = uuid4().hex
    return {
        "id": document_id,
        "filename": filename,
        "saved_path": str(saved_path),
        "file_size": file_size,
        "status": status,
        "policy_score": policy["score"],
        "policy_reason": policy["reason"],
        "matched_keywords": policy["matched_keywords"],
        "chunk_count": chunk_count,
        "text_preview": text[:300],
        "uploaded_at": now,
        "updated_at": now,
    }

class DocumentStore:
    def __init__(self, path):
        self.path = Path(path)

    def list(self):
        return read_json(self.path, [])

    def save_all(self, documents):
        write_json(self.path, documents)

    def get(self, document_id):
        for document in self.list():
            if document["id"] == document_id:
                return document
        return None

    def add(self, document):
        documents = self.list()
        documents.append(document)
        self.save_all(documents)
        return document

    def update(self, document_id, **changes):
        documents = self.list()
        for index, document in enumerate(documents):
            if document["id"] == document_id:
                updated = {**document, **changes, "updated_at": utc_now()}
                documents[index] = updated
                self.save_all(documents)
                return updated
        return None

    def delete(self, document_id):
        documents = self.list()
        kept = [document for document in documents if document["id"] != document_id]
        if len(kept) == len(documents):
            return None
        self.save_all(kept)
        return True

def save_uploaded_file(upload_dir, filename, content):
    upload_dir = Path(upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    clean_name = safe_filename(filename)
    saved_name = f"{uuid4().hex}_{clean_name}"
    saved_path = upload_dir / saved_name
    saved_path.write_bytes(content)
    return saved_path
