def normalize_uploaded_files(uploaded_files):
    if not uploaded_files:
        return []
    if isinstance(uploaded_files, (list, tuple)):
        return list(uploaded_files)
    return [uploaded_files]


def build_document_rows(documents):
    rows = []
    for document in documents:
        document_id = document.get("id", "")
        rows.append({
            "id": document_id,
            "short_id": document_id[:8],
            "filename": document.get("filename", ""),
            "status": document.get("status", "unknown"),
            "chunks": document.get("chunk_count", 0),
            "score": document.get("policy_score", 0),
            "updated_at": document.get("updated_at", ""),
        })
    return rows


def document_search_text(document):
    values = [
        document.get("filename", ""),
        document.get("status", ""),
        document.get("policy_reason", ""),
        " ".join(document.get("matched_keywords", [])),
    ]
    return " ".join(values).lower()


def filter_documents(documents, status_filter="All", search_text=""):
    search_text = search_text.strip().lower()
    filtered = []
    for document in documents:
        if status_filter != "All" and document.get("status") != status_filter:
            continue
        if search_text and search_text not in document_search_text(document):
            continue
        filtered.append(document)
    return filtered
