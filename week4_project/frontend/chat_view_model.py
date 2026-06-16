import re
import unicodedata


INITIAL_SUGGESTIONS = [
    "CEO Hà Nội là ai?",
    "Nội quy công ty gồm những gì?",
    "Chính sách nghỉ phép thế nào?",
    "Công ty có những chính sách nào?",
]

GENERAL_FOLLOWUP_SUGGESTIONS = [
    "Công ty có những chính sách nào?",
    "Tóm tắt các nội quy quan trọng",
    "Có tài liệu nào mới được cập nhật?",
]

TOPIC_FOLLOWUP_SUGGESTIONS = [
    (
        {"ceo", "ha noi", "hanoi", "hn", "ban dieu hanh", "executive"},
        [
            "Ban điều hành BnK gồm những ai?",
            "Vai trò của CEO BnK HN là gì?",
            "Các quyết định bổ nhiệm năm 2025 gồm những ai?",
        ],
    ),
    (
        {"nghi phep", "leave", "nghi", "phep"},
        [
            "Quy trình xin nghỉ phép thế nào?",
            "Một năm có bao nhiêu ngày phép?",
            "Nghỉ phép cần được ai phê duyệt?",
        ],
    ),
    (
        {"noi quy", "quy dinh", "policy", "chinh sach"},
        [
            "Tóm tắt các nội quy quan trọng",
            "Nhân viên cần tuân thủ quy định nào?",
            "Chính sách nào liên quan đến nhân sự?",
        ],
    ),
]


def normalize_text(text):
    lowered = str(text).lower().replace("đ", "d")
    decomposed = unicodedata.normalize("NFD", lowered)
    without_marks = "".join(
        char for char in decomposed
        if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9_]+", " ", without_marks)).strip()


def hide_source_citations(text):
    without_inline_sources = re.sub(
        r"\s*\[(?:Source|Sources):[^\]]+\]",
        "",
        str(text),
        flags=re.IGNORECASE,
    )
    without_source_lines = re.sub(
        r"(?im)^\s*Sources?:\s*.+$",
        "",
        without_inline_sources,
    )
    without_spaced_punctuation = re.sub(r"\s+([.,;:!?])", r"\1", without_source_lines)
    return re.sub(r"\n{3,}", "\n\n", without_spaced_punctuation).strip()


def build_visible_message(message):
    visible_message = message.copy()
    visible_message.pop("sources", None)
    visible_message["content"] = hide_source_citations(visible_message.get("content", ""))
    return visible_message


def build_visible_messages(session_messages, pending_question):
    visible_messages = [build_visible_message(message) for message in session_messages]
    if pending_question:
        visible_messages.append({
            "role": "user",
            "content": pending_question,
            "pending": True,
        })
    return visible_messages


def should_show_empty_state(session_messages, pending_question):
    return not session_messages and not pending_question


def get_initial_suggestions():
    return list(INITIAL_SUGGESTIONS)


def last_user_question(messages):
    for message in reversed(messages):
        if message.get("role") == "user":
            return message.get("content", "")
    return ""


def get_followup_suggestions(messages):
    normalized_question = normalize_text(last_user_question(messages))

    for keywords, suggestions in TOPIC_FOLLOWUP_SUGGESTIONS:
        if any(keyword in normalized_question for keyword in keywords):
            return list(suggestions)

    return list(GENERAL_FOLLOWUP_SUGGESTIONS)


def next_active_session_id_after_delete(sessions, active_session_id, deleted_session_id):
    remaining_session_ids = [
        session["id"]
        for session in sessions
        if session.get("id") != deleted_session_id
    ]

    if active_session_id != deleted_session_id and active_session_id in remaining_session_ids:
        return active_session_id

    return remaining_session_ids[0] if remaining_session_ids else None
