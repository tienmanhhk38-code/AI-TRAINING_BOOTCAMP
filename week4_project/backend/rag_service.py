import re
import unicodedata
from collections import Counter

from backend.document_policy import is_company_question
from backend.search_utils import relevance_score, tokenize

MIN_RELEVANCE_SCORE = 0.18
GREETING_WORDS = {"hi", "hello", "hey", "chao", "xin chao"}
IDENTITY_PATTERNS = {
    "ban la ai",
    "ban la gi",
    "m la ai",
    "may la ai",
    "who are you",
    "what are you",
    "gioi thieu",
    "gioi thieu ve ban",
}

def embed_text(text):
    return Counter(tokenize(text))

def chunk_text(text, source, chunk_size=500, overlap=50, document_id=None):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap must be greater than or equal to 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    index = 1
    cleaned = clean_text(text)

    while start < len(cleaned):
        end = min(start + chunk_size, len(cleaned))
        chunk = cleaned[start:end].strip()

        if chunk:
            chunk_id_prefix = document_id or source
            chunks.append({
                "chunk_id": f"{chunk_id_prefix}:c{index}",
                "document_id": document_id,
                "source": source,
                "text": chunk,
            })
            index += 1

        if end == len(cleaned):
            break

        start = end - overlap

    return chunks

def clean_text(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return re.sub(r"[ \t]+", " ", "\n".join(lines))

def normalize_intent(text):
    decomposed = unicodedata.normalize("NFD", text.lower())
    without_marks = "".join(
        char for char in decomposed
        if unicodedata.category(char) != "Mn"
    )
    without_marks = without_marks.replace("đ", "d").replace("Đ", "D")
    return " ".join(re.findall(r"[a-z0-9_]+", without_marks))

def is_greeting(question):
    normalized = normalize_intent(question)
    return normalized in GREETING_WORDS

def is_identity_question(question):
    normalized = normalize_intent(question)
    return normalized in IDENTITY_PATTERNS

def greeting_answer():
    return "Hi! I am Bnk Chatbot. You can ask about BNK company documents or general questions."

def identity_answer():
    return "I am Bnk Chatbot, an internal assistant for BNK company documents. I can help answer questions about approved company policies, rules, procedures, and general questions."

def gemini_unavailable_answer():
    return "Gemini is not responding right now. Please try again in a moment."

def hide_source_citations(text):
    without_inline_sources = re.sub(
        r"\s*\[(?:Source|Sources):[^\]]+\]",
        "",
        text,
        flags=re.IGNORECASE,
    )
    without_source_lines = re.sub(
        r"(?im)^\s*Sources?:\s*.+$",
        "",
        without_inline_sources,
    )
    without_spaced_punctuation = re.sub(r"\s+([.,;:!?])", r"\1", without_source_lines)
    return re.sub(r"\n{3,}", "\n\n", without_spaced_punctuation).strip()

class RAGService:
    def __init__(self, chunks=None, llm_client=None, vector_store=None):
        self.chunks = []
        self.index = []
        self.llm_client = llm_client
        self.vector_store = vector_store
        self.set_chunks(chunks or [])

    def set_chunks(self, chunks):
        self.chunks = list(chunks)
        self.index = [
            {
                "chunk": chunk,
                "embedding": embed_text(chunk.get("text", "")),
            }
            for chunk in self.chunks
        ]
        if self.vector_store:
            self.vector_store.reset(self.chunks)

    def add_text(self, text, source, document_id=None):
        new_chunks = chunk_text(text, source=source, document_id=document_id)
        self.set_chunks(self.chunks + new_chunks)
        return new_chunks

    def remove_document(self, document_id):
        self.set_chunks([
            chunk for chunk in self.chunks
            if chunk.get("document_id") != document_id
        ])

    def replace_document(self, text, source, document_id):
        kept_chunks = [
            chunk for chunk in self.chunks
            if chunk.get("document_id") != document_id
        ]
        new_chunks = chunk_text(text, source=source, document_id=document_id)
        self.set_chunks(kept_chunks + new_chunks)
        return new_chunks

    def _local_retrieve(self, question, top_k):
        results = []

        for item in self.index:
            score = relevance_score(question, item["chunk"].get("text", ""))
            if score > 0:
                results.append({
                    "chunk_id": item["chunk"]["chunk_id"],
                    "source": item["chunk"]["source"],
                    "text": item["chunk"]["text"],
                    "score": round(score, 4),
                })

        results.sort(key=lambda item: item["score"], reverse=True)
        return results[:top_k]

    def _merge_contexts(self, question, vector_contexts, local_contexts, top_k):
        combined = {}

        for context in vector_contexts:
            vector_score = context.get("score", 0)
            if vector_score < MIN_RELEVANCE_SCORE:
                continue

            local_score = relevance_score(question, context.get("text", ""))
            score = local_score + (min(vector_score, 1.0) * 0.05) if local_score > 0 else vector_score
            combined[context["chunk_id"]] = {
                **context,
                "score": round(score, 4),
            }

        for context in local_contexts:
            current = combined.get(context["chunk_id"])
            if not current or context["score"] > current.get("score", 0):
                combined[context["chunk_id"]] = context

        results = list(combined.values())
        results.sort(key=lambda item: item["score"], reverse=True)
        return results[:top_k]

    def retrieve(self, question, top_k=3):
        search_limit = max(top_k, 8)
        local_contexts = self._local_retrieve(question, search_limit)
        vector_contexts = []

        if self.vector_store:
            try:
                vector_contexts = self.vector_store.query(question, top_k=search_limit)
            except Exception:
                vector_contexts = []

        return self._merge_contexts(question, vector_contexts, local_contexts, top_k)

    def ask(self, question, top_k=3, history=None, current_date=None):
        if not question.strip():
            return {
                "answer": "Question is empty.",
                "sources": [],
                "contexts": [],
                "llm": "local",
            }

        if is_greeting(question):
            return {
                "answer": greeting_answer(),
                "sources": [],
                "contexts": [],
                "llm": "local_greeting",
            }

        if is_identity_question(question):
            return {
                "answer": identity_answer(),
                "sources": [],
                "contexts": [],
                "llm": "local_identity",
            }

        contexts = self.retrieve(question, top_k=top_k)
        if not contexts:
            if self.llm_client:
                if is_company_question(question):
                    return {
                        "answer": "I cannot find this information in approved BNK company documents yet.",
                        "sources": [],
                        "contexts": [],
                        "llm": "gemini_no_context",
                    }

                try:
                    answer = self.llm_client.generate_general_answer(
                        question,
                        history=history,
                        current_date=current_date,
                    )
                except Exception:
                    return {
                        "answer": gemini_unavailable_answer(),
                        "sources": [],
                        "contexts": [],
                        "llm": "local_fallback",
                    }

                return {
                    "answer": answer,
                    "sources": [],
                    "contexts": [],
                    "llm": "gemini_general",
                }

            return {
                "answer": "I do not know from the indexed documents.",
                "sources": [],
                "contexts": [],
                "llm": "local",
            }

        best_context = contexts[0]
        sources = [context["chunk_id"] for context in contexts]

        if self.llm_client:
            try:
                answer = self.llm_client.generate_answer(
                    question,
                    contexts,
                    history=history,
                    current_date=current_date,
                )
                answer = hide_source_citations(answer)
            except Exception:
                return {
                    "answer": f"{gemini_unavailable_answer()} Based on approved documents: {best_context['text']}",
                    "sources": sources,
                    "contexts": contexts,
                    "llm": "local_fallback",
                }

            return {
                "answer": answer,
                "sources": sources,
                "contexts": contexts,
                "llm": "gemini",
            }

        return {
            "answer": f"Based on the indexed documents, {best_context['text']}",
            "sources": sources,
            "contexts": contexts,
            "llm": "local",
        }
