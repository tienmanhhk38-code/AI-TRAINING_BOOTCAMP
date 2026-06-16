from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from backend.storage import read_json, write_json

DEFAULT_SESSION_TITLE = "New chat"

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def title_from_question(question):
    title = " ".join(question.strip().split())
    if not title:
        return DEFAULT_SESSION_TITLE
    return title if len(title) <= 38 else title[:35].rstrip() + "..."

def build_message(role, content, sources=None, llm=None):
    message = {
        "role": role,
        "content": content,
        "created_at": utc_now(),
    }
    if sources is not None:
        message["sources"] = sources
    if llm is not None:
        message["llm"] = llm
    return message

class ChatSessionStore:
    def __init__(self, path):
        self.path = Path(path)

    def list(self):
        sessions = read_json(self.path, [])
        return sorted(sessions, key=lambda session: session.get("updated_at", ""), reverse=True)

    def save_all(self, sessions):
        write_json(self.path, sessions)

    def list_summaries(self):
        return [
            {
                "id": session["id"],
                "title": session["title"],
                "message_count": len(session.get("messages", [])),
                "created_at": session["created_at"],
                "updated_at": session["updated_at"],
            }
            for session in self.list()
        ]

    def create(self, title=DEFAULT_SESSION_TITLE):
        now = utc_now()
        session = {
            "id": uuid4().hex,
            "title": title or DEFAULT_SESSION_TITLE,
            "messages": [],
            "created_at": now,
            "updated_at": now,
        }
        sessions = self.list()
        sessions.append(session)
        self.save_all(sessions)
        return session

    def get(self, session_id):
        for session in self.list():
            if session["id"] == session_id:
                return session
        return None

    def update(self, session):
        sessions = self.list()
        for index, current in enumerate(sessions):
            if current["id"] == session["id"]:
                sessions[index] = session
                self.save_all(sessions)
                return session
        sessions.append(session)
        self.save_all(sessions)
        return session

    def clear(self, session_id):
        session = self.get(session_id)
        if not session:
            return None
        session["messages"] = []
        session["updated_at"] = utc_now()
        return self.update(session)

    def delete(self, session_id):
        sessions = self.list()
        kept = [session for session in sessions if session["id"] != session_id]
        if len(kept) == len(sessions):
            return None
        self.save_all(kept)
        return True

    def add_exchange(self, session_id, question, answer_record):
        session = self.get(session_id) if session_id else None
        if not session:
            session = self.create()

        messages = session.get("messages", [])
        if session["title"] == DEFAULT_SESSION_TITLE and not messages:
            session["title"] = title_from_question(question)

        messages.append(build_message("user", question))
        messages.append(build_message(
            "assistant",
            answer_record["answer"],
            sources=answer_record.get("sources", []),
            llm=answer_record.get("llm"),
        ))
        session["messages"] = messages
        session["updated_at"] = utc_now()
        return self.update(session)
