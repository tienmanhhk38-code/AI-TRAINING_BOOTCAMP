from html import escape

import requests
import streamlit as st

from frontend.admin_view_model import build_document_rows, filter_documents, normalize_uploaded_files
from frontend.chat_view_model import (
    build_visible_messages,
    get_followup_suggestions,
    get_initial_suggestions,
    next_active_session_id_after_delete,
    should_show_empty_state,
)
from frontend.config import get_api_base_url

API_BASE_URL = get_api_base_url()
SUPPORTED_TYPES = ["txt", "md", "csv", "pdf", "docx", "xlsx", "xlsm"]

st.set_page_config(page_title="Bnk Chatbot", layout="wide", initial_sidebar_state="expanded")

def apply_theme():
    st.markdown(
        """
        <style>
        :root {
            --bnk-bg: #191918;
            --bnk-panel-2: #2b2b2a;
            --bnk-border: #333331;
            --bnk-text: #f4f2ec;
            --bnk-muted: #aaa69d;
            --bnk-chat-width: 900px;
            --bnk-chat-pad: 32px;
        }

        .stApp {
            background: var(--bnk-bg);
            color: var(--bnk-text);
        }

        section[data-testid="stSidebar"] {
            background: #161615;
            border-right: 1px solid var(--bnk-border);
        }

        section[data-testid="stSidebar"] * {
            color: var(--bnk-text);
        }

        .main .block-container,
        section[data-testid="stMain"] .block-container,
        div[data-testid="stMainBlockContainer"] {
            box-sizing: border-box;
            width: 100%;
            max-width: var(--bnk-chat-width);
            margin-left: auto;
            margin-right: auto;
            padding-left: var(--bnk-chat-pad);
            padding-right: var(--bnk-chat-pad);
            padding-top: 72px;
            padding-bottom: 126px;
        }

        h1, h2, h3 {
            letter-spacing: 0;
        }

        [data-testid="stChatMessage"] {
            background: transparent;
            padding: 10px 0;
        }

        [data-testid="stChatMessageContent"] {
            max-width: 720px;
        }

        [data-testid="stChatInput"] {
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 auto;
        }

        div[data-testid="stBottomBlockContainer"],
        div[data-testid="stBottom"] > div {
            box-sizing: border-box;
            width: 100%;
            max-width: var(--bnk-chat-width);
            margin-left: auto;
            margin-right: auto;
            padding-left: var(--bnk-chat-pad);
            padding-right: var(--bnk-chat-pad);
        }

        [data-testid="stChatInput"] [data-baseweb="textarea"],
        [data-testid="stChatInput"] textarea {
            width: 100% !important;
        }

        [data-testid="stChatInput"] textarea {
            background: var(--bnk-panel-2);
            color: var(--bnk-text);
            border: 1px solid var(--bnk-border);
            border-radius: 18px;
            min-height: 72px;
        }

        .bnk-typing {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            width: fit-content;
            background: var(--bnk-panel-2);
            border: 1px solid var(--bnk-border);
            border-radius: 18px;
            padding: 12px 14px;
        }

        .bnk-typing span {
            width: 7px;
            height: 7px;
            border-radius: 999px;
            background: var(--bnk-muted);
            animation: bnkTyping 1.15s infinite ease-in-out;
        }

        .bnk-typing span:nth-child(2) {
            animation-delay: 0.16s;
        }

        .bnk-typing span:nth-child(3) {
            animation-delay: 0.32s;
        }

        @keyframes bnkTyping {
            0%, 80%, 100% {
                opacity: 0.35;
                transform: translateY(0);
            }
            40% {
                opacity: 1;
                transform: translateY(-3px);
            }
        }

        .bnk-topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 28px;
        }

        .bnk-title {
            font-size: 18px;
            font-weight: 700;
        }

        .bnk-badge {
            background: #10100f;
            color: var(--bnk-muted);
            border-radius: 12px;
            padding: 7px 10px;
            font-size: 13px;
        }

        .bnk-admin-hero {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            gap: 24px;
            margin-bottom: 24px;
        }

        .bnk-admin-eyebrow {
            color: var(--bnk-muted);
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .bnk-admin-title {
            font-size: 34px;
            line-height: 1.1;
            font-weight: 800;
        }

        .bnk-admin-subtitle {
            color: var(--bnk-muted);
            font-size: 14px;
            margin-top: 8px;
            max-width: 620px;
        }

        .bnk-admin-status {
            color: var(--bnk-muted);
            background: #10100f;
            border: 1px solid var(--bnk-border);
            border-radius: 10px;
            padding: 10px 12px;
            font-size: 13px;
            white-space: nowrap;
        }

        .bnk-metric-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
            margin-bottom: 24px;
        }

        .bnk-metric-card {
            border: 1px solid var(--bnk-border);
            background: #20201f;
            border-radius: 8px;
            padding: 14px;
        }

        .bnk-metric-label {
            color: var(--bnk-muted);
            font-size: 12px;
        }

        .bnk-metric-value {
            font-size: 26px;
            font-weight: 750;
            margin-top: 6px;
        }

        .bnk-section-title {
            font-size: 18px;
            font-weight: 750;
            margin: 8px 0 6px;
        }

        .bnk-section-subtitle {
            color: var(--bnk-muted);
            font-size: 13px;
            margin-bottom: 12px;
        }

        .bnk-upload-summary {
            border: 1px solid var(--bnk-border);
            background: #20201f;
            border-radius: 8px;
            padding: 12px 14px;
            margin: 10px 0 14px;
        }

        .bnk-document-detail {
            border: 1px solid var(--bnk-border);
            background: #20201f;
            border-radius: 8px;
            padding: 16px;
            margin-top: 8px;
        }

        .bnk-document-title {
            font-size: 18px;
            font-weight: 750;
            overflow-wrap: anywhere;
        }

        .bnk-document-meta {
            color: var(--bnk-muted);
            font-size: 12px;
            margin-top: 8px;
        }

        .bnk-status-pill {
            display: inline-block;
            border: 1px solid var(--bnk-border);
            border-radius: 999px;
            padding: 4px 9px;
            font-size: 12px;
            margin-top: 10px;
        }

        .bnk-empty-admin {
            border: 1px dashed var(--bnk-border);
            border-radius: 8px;
            padding: 28px;
            color: var(--bnk-muted);
            text-align: center;
        }

        .bnk-empty {
            min-height: 48vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 8px;
        }

        .bnk-empty-title {
            font-size: 28px;
            font-weight: 750;
        }

        .bnk-empty-subtitle {
            color: var(--bnk-muted);
            font-size: 15px;
        }

        .bnk-suggestions {
            margin: 18px 0 4px;
        }

        .bnk-suggestions-title {
            color: var(--bnk-muted);
            font-size: 13px;
            margin-bottom: 10px;
        }

        .bnk-sidebar-brand {
            font-size: 25px;
            font-weight: 800;
            margin: 2px 0 18px;
        }

        .bnk-sidebar-label {
            color: var(--bnk-muted);
            font-size: 12px;
            margin-top: 18px;
            margin-bottom: 6px;
            text-transform: uppercase;
        }

        div[data-testid="stButton"] > button {
            border-radius: 8px;
            border: 0;
            background: transparent;
            color: var(--bnk-text);
            justify-content: flex-start;
            width: 100%;
        }

        div[data-testid="stButton"] > button:hover {
            background: #242421;
            color: var(--bnk-text);
        }

        div[data-testid="stButton"] > button[kind="primary"] {
            background: #2a2a28;
            color: var(--bnk-text);
        }

        section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:has(button[title="Delete chat"]) button[title="Delete chat"],
        section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:has(button[aria-label="Delete chat"]) button[aria-label="Delete chat"] {
            opacity: 0;
            color: #ff6b6b !important;
            background: transparent !important;
            border: 1px solid transparent !important;
            transition: opacity 120ms ease, background 120ms ease, border-color 120ms ease;
            justify-content: center;
        }

        section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:has(button[title="Delete chat"]):hover button[title="Delete chat"],
        section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:has(button[aria-label="Delete chat"]):hover button[aria-label="Delete chat"],
        section[data-testid="stSidebar"] button[title="Delete chat"]:focus,
        section[data-testid="stSidebar"] button[aria-label="Delete chat"]:focus {
            opacity: 1;
        }

        section[data-testid="stSidebar"] button[title="Delete chat"]:hover,
        section[data-testid="stSidebar"] button[aria-label="Delete chat"]:hover {
            color: #ffffff !important;
            background: #9f1d1d !important;
            border-color: #b91c1c !important;
        }

        @media (max-width: 900px) {
            :root {
                --bnk-chat-pad: 18px;
            }

            .main .block-container,
            section[data-testid="stMain"] .block-container,
            div[data-testid="stMainBlockContainer"] {
                max-width: 100%;
            }

            .bnk-admin-hero {
                align-items: flex-start;
                flex-direction: column;
            }

            .bnk-metric-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def api_get(path):
    response = requests.get(f"{API_BASE_URL}{path}", timeout=20)
    response.raise_for_status()
    return response.json()

def api_post(path, timeout=90, **kwargs):
    response = requests.post(f"{API_BASE_URL}{path}", timeout=timeout, **kwargs)
    response.raise_for_status()
    return response.json()

def api_delete(path):
    response = requests.delete(f"{API_BASE_URL}{path}", timeout=30)
    response.raise_for_status()
    return response.json()

def refresh_sessions():
    try:
        st.session_state.chat_sessions = api_get("/chat/sessions")
    except requests.RequestException:
        st.session_state.chat_sessions = []
        return

    session_ids = {session["id"] for session in st.session_state.chat_sessions}
    if st.session_state.active_session_id not in session_ids:
        st.session_state.active_session_id = (
            st.session_state.chat_sessions[0]["id"]
            if st.session_state.chat_sessions
            else None
        )

def create_session(title="New chat"):
    try:
        session = api_post("/chat/sessions", timeout=5, json={"title": title})
    except requests.RequestException as error:
        st.error(f"Cannot create chat session: {error}")
        return None
    st.session_state.active_session_id = session["id"]
    refresh_sessions()
    return session

def delete_chat_session(session_id):
    try:
        api_delete(f"/chat/sessions/{session_id}")
    except requests.RequestException as error:
        st.error(f"Cannot delete chat session: {error}")
        return

    st.session_state.active_session_id = next_active_session_id_after_delete(
        st.session_state.chat_sessions,
        active_session_id=st.session_state.active_session_id,
        deleted_session_id=session_id,
    )
    st.session_state.pending_delete_session_id = None
    refresh_sessions()
    if not st.session_state.active_session_id:
        create_session("New chat")
    st.session_state.active_page = "Chatbot"
    st.rerun()

@st.dialog("Delete this chat?")
def render_delete_session_dialog():
    session_id = st.session_state.get("pending_delete_session_id")
    if not session_id:
        return

    session = next(
        (item for item in st.session_state.chat_sessions if item.get("id") == session_id),
        {"title": "this chat"},
    )
    st.write(f"Delete '{session.get('title', 'this chat')}'? This cannot be undone.")
    cancel_col, delete_col = st.columns(2)
    with cancel_col:
        if st.button("Cancel", use_container_width=True):
            st.session_state.pending_delete_session_id = None
            st.rerun()
    with delete_col:
        if st.button("Delete chat", type="primary", use_container_width=True):
            delete_chat_session(session_id)

def init_state():
    if "active_page" not in st.session_state:
        st.session_state.active_page = "Chatbot"
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = []
    if "active_session_id" not in st.session_state:
        st.session_state.active_session_id = None
    if "pending_delete_session_id" not in st.session_state:
        st.session_state.pending_delete_session_id = None
    refresh_sessions()
    if not st.session_state.active_session_id:
        create_session("New chat")

def current_session():
    session_id = st.session_state.active_session_id
    if not session_id:
        return {"id": None, "title": "New chat", "messages": []}
    try:
        return api_get(f"/chat/sessions/{session_id}")
    except requests.RequestException:
        return {"id": None, "title": "New chat", "messages": []}

def set_page(page):
    st.session_state.active_page = page
    st.rerun()

def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="bnk-sidebar-brand">Bnk Chatbot</div>', unsafe_allow_html=True)

        if st.button("+  New chat", key="new_chat"):
            create_session("New chat")
            st.session_state.active_page = "Chatbot"
            st.rerun()

        st.markdown('<div class="bnk-sidebar-label">Functions</div>', unsafe_allow_html=True)
        if st.button("Chatbot", key="nav_chatbot", type="primary" if st.session_state.active_page == "Chatbot" else "secondary"):
            set_page("Chatbot")
        if st.button("Admin documents", key="nav_admin", type="primary" if st.session_state.active_page == "Admin" else "secondary"):
            set_page("Admin")

        st.markdown('<div class="bnk-sidebar-label">Recents</div>', unsafe_allow_html=True)
        for session in st.session_state.chat_sessions:
            session_id = session["id"]
            title = session["title"]
            is_active = session_id == st.session_state.active_session_id
            button_type = "primary" if is_active and st.session_state.active_page == "Chatbot" else "secondary"
            session_col, delete_col = st.columns([0.75, 0.25], gap="small")
            with session_col:
                if st.button(title, key=f"session_{session_id}", type=button_type):
                    st.session_state.active_session_id = session_id
                    st.session_state.active_page = "Chatbot"
                    st.session_state.pending_delete_session_id = None
                    st.rerun()
            with delete_col:
                if st.button("x", key=f"delete_session_{session_id}", help="Delete chat", use_container_width=True):
                    st.session_state.pending_delete_session_id = session_id

        if st.session_state.pending_delete_session_id:
            render_delete_session_dialog()

def load_documents():
    try:
        return api_get("/documents")
    except requests.RequestException as error:
        st.error(f"Cannot load documents: {error}")
        return []

def render_chat_header(session):
    title = escape(session["title"])
    st.markdown(
        f"""
        <div class="bnk-topbar">
            <div class="bnk-title">{title}</div>
            <div class="bnk-badge">Gemini + ChromaDB</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_empty_chat():
    st.markdown(
        """
        <div class="bnk-empty">
            <div class="bnk-empty-title">How can I help?</div>
            <div class="bnk-empty-subtitle">Ask about BNK company documents, policies, procedures, or general topics.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_typing_indicator(slot):
    slot.markdown(
        """
        <div class="bnk-typing" aria-label="AI is typing">
            <span></span>
            <span></span>
            <span></span>
        </div>
        """,
        unsafe_allow_html=True,
    )

def choose_suggestion(question):
    st.session_state.suggested_question = question
    st.rerun()

def pop_suggested_question():
    if "suggested_question" not in st.session_state:
        return None
    return st.session_state.pop("suggested_question")

def render_suggestion_buttons(title, suggestions, key_prefix):
    if not suggestions:
        return

    st.markdown(
        f"""
        <div class="bnk-suggestions">
            <div class="bnk-suggestions-title">{escape(title)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for row_index in range(0, len(suggestions), 3):
        row = suggestions[row_index:row_index + 3]
        columns = st.columns(len(row))
        for column_index, suggestion in enumerate(row):
            with columns[column_index]:
                button_key = f"{key_prefix}_{row_index}_{column_index}"
                if st.button(suggestion, key=button_key, use_container_width=True):
                    choose_suggestion(suggestion)

def render_chatbot_page():
    session = current_session()
    render_chat_header(session)

    messages = session.get("messages", [])
    suggested_question = pop_suggested_question()
    typed_question = st.chat_input("Write a message...")
    question = suggested_question or typed_question

    if should_show_empty_state(messages, question):
        render_empty_chat()

    for message in build_visible_messages(messages, question):
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if not question:
        if not messages:
            render_suggestion_buttons(
                "Câu hỏi thường gặp",
                get_initial_suggestions(),
                "initial_suggestion",
            )
        elif messages[-1].get("role") == "assistant":
            render_suggestion_buttons(
                "Có thể bạn quan tâm",
                get_followup_suggestions(messages),
                f"followup_suggestion_{session.get('id', 'new')}_{len(messages)}",
            )
        return

    typing_slot = None
    with st.chat_message("assistant"):
        typing_slot = st.empty()
        render_typing_indicator(typing_slot)

    try:
        data = api_post("/ask", json={
            "question": question,
            "session_id": session.get("id"),
        })
    except requests.RequestException as error:
        if typing_slot:
            typing_slot.empty()
        st.error(f"Cannot ask chatbot: {error}")
        return

    st.session_state.active_session_id = data["session_id"]
    refresh_sessions()
    st.rerun()

def render_admin_header(health):
    llm_model = escape(health.get("llm_model", health.get("llm", "unknown")))
    st.markdown(
        f"""
        <div class="bnk-admin-hero">
            <div>
                <div class="bnk-admin-eyebrow">Knowledge base</div>
                <div class="bnk-admin-title">Admin documents</div>
                <div class="bnk-admin-subtitle">
                    Upload, review, replace, and index BNK company documents for chatbot retrieval.
                </div>
            </div>
            <div class="bnk-admin-status">Model: {llm_model}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_admin_metrics(health):
    metrics = [
        ("Documents", health.get("document_count", 0)),
        ("Chunks", health.get("chunk_count", 0)),
        ("Vector DB", health.get("vector_db", "local")),
        ("LLM", health.get("llm", "local")),
    ]
    columns = st.columns(4)
    for column, (label, value) in zip(columns, metrics):
        with column:
            st.markdown(
                f"""
<div class="bnk-metric-card">
    <div class="bnk-metric-label">{escape(str(label))}</div>
    <div class="bnk-metric-value">{escape(str(value))}</div>
</div>
""",
                unsafe_allow_html=True,
            )
    st.markdown(
        """
<div style="height: 18px;"></div>
""",
        unsafe_allow_html=True,
    )

def render_upload_results():
    results = st.session_state.get("last_upload_results", [])
    if not results:
        return

    st.markdown('<div class="bnk-section-title">Last upload results</div>', unsafe_allow_html=True)
    st.dataframe(results, use_container_width=True, hide_index=True)

def upload_document_file(uploaded_file):
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type or "application/octet-stream",
        )
    }
    result = api_post("/documents/upload", files=files)
    document = result["document"]
    return {
        "filename": document["filename"],
        "status": document["status"],
        "chunks": document.get("chunk_count", 0),
        "message": document.get("policy_reason", ""),
    }

def render_upload_panel():
    st.markdown('<div class="bnk-section-title">Upload queue</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="bnk-section-subtitle">Choose multiple PDF, Word, Excel, CSV, Markdown, or TXT files.</div>',
        unsafe_allow_html=True,
    )

    uploaded_files = normalize_uploaded_files(st.file_uploader(
        "Upload documents",
        type=SUPPORTED_TYPES,
        accept_multiple_files=True,
        label_visibility="collapsed",
    ))

    if uploaded_files:
        file_rows = [
            {
                "filename": file.name,
                "type": file.type or "application/octet-stream",
                "size_kb": round(len(file.getvalue()) / 1024, 1),
            }
            for file in uploaded_files
        ]
        st.markdown(
            f'<div class="bnk-upload-summary">{len(uploaded_files)} file(s) ready to upload</div>',
            unsafe_allow_html=True,
        )
        st.dataframe(file_rows, use_container_width=True, hide_index=True)

    render_upload_results()

    if not uploaded_files:
        return

    if st.button(f"Upload {len(uploaded_files)} document(s)", type="primary", use_container_width=True):
        progress = st.progress(0)
        results = []
        for index, uploaded_file in enumerate(uploaded_files, start=1):
            try:
                results.append(upload_document_file(uploaded_file))
            except requests.RequestException as error:
                results.append({
                    "filename": uploaded_file.name,
                    "status": "failed",
                    "chunks": 0,
                    "message": str(error),
                })
            progress.progress(index / len(uploaded_files))

        st.session_state.last_upload_results = results
        st.rerun()

def render_document_table(documents):
    if not documents:
        st.markdown(
            '<div class="bnk-empty-admin">No documents yet. Upload company files to start building the chatbot knowledge base.</div>',
            unsafe_allow_html=True,
        )
        return

    st.dataframe(build_document_rows(documents), use_container_width=True, hide_index=True)

def render_document_detail(selected):
    st.markdown(
        f"""
        <div class="bnk-document-detail">
            <div class="bnk-document-title">{escape(selected.get("filename", ""))}</div>
            <div class="bnk-status-pill">{escape(selected.get("status", "unknown"))}</div>
            <div class="bnk-document-meta">
                ID {escape(selected.get("id", "")[:8])} &middot;
                Chunks {selected.get("chunk_count", 0)} &middot;
                Score {selected.get("policy_score", 0)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    reason = selected.get("policy_reason", "")
    if reason:
        st.caption(reason)
    if selected.get("matched_keywords"):
        st.caption("Matched: " + ", ".join(selected["matched_keywords"]))
    if selected.get("text_preview"):
        st.text_area("Preview", selected["text_preview"], height=150, disabled=True)

def render_document_actions(selected):
    action_cols = st.columns(3)
    with action_cols[0]:
        if st.button("Approve & index", disabled=selected["status"] == "approved", use_container_width=True):
            try:
                api_post(f"/documents/{selected['id']}/approve")
                st.success("Approved")
                st.rerun()
            except requests.RequestException as error:
                st.error(f"Approve failed: {error}")
    with action_cols[1]:
        if st.button("Re-index", use_container_width=True):
            try:
                api_post(f"/documents/{selected['id']}/reindex")
                st.success("Re-indexed")
                st.rerun()
            except requests.RequestException as error:
                st.error(f"Re-index failed: {error}")
    with action_cols[2]:
        if st.button("Delete", type="secondary", use_container_width=True):
            try:
                api_delete(f"/documents/{selected['id']}")
                st.success("Deleted")
                st.rerun()
            except requests.RequestException as error:
                st.error(f"Delete failed: {error}")

    replacement = st.file_uploader(
        "Replace selected document",
        type=SUPPORTED_TYPES,
        key=f"replace_file_{selected['id']}",
    )
    if replacement and st.button("Replace document", use_container_width=True):
        files = {
            "file": (
                replacement.name,
                replacement.getvalue(),
                replacement.type or "application/octet-stream",
            )
        }
        try:
            api_post(f"/documents/{selected['id']}/replace", files=files)
            st.success("Replaced")
            st.rerun()
        except requests.RequestException as error:
            st.error(f"Replace failed: {error}")

def render_document_library(documents):
    st.markdown('<div class="bnk-section-title">Document library</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="bnk-section-subtitle">Filter status, search filename/keywords, then open a document for review.</div>',
        unsafe_allow_html=True,
    )

    statuses = ["All"] + sorted({document.get("status", "unknown") for document in documents})
    filter_cols = st.columns([1, 2])
    with filter_cols[0]:
        status_filter = st.selectbox("Status", statuses)
    with filter_cols[1]:
        search_text = st.text_input("Search", placeholder="Search filename, status, keyword")

    filtered_documents = filter_documents(documents, status_filter=status_filter, search_text=search_text)
    library_col, detail_col = st.columns([1.45, 1])
    with library_col:
        render_document_table(filtered_documents)

    with detail_col:
        if not filtered_documents:
            return
        labels = [
            f"{document['filename']} | {document.get('status', 'unknown')} | {document['id'][:8]}"
            for document in filtered_documents
        ]
        selected_label = st.selectbox("Open document", labels)
        selected = filtered_documents[labels.index(selected_label)]
        render_document_detail(selected)
        render_document_actions(selected)

def render_admin_page():
    try:
        health = api_get("/health")
    except requests.RequestException as error:
        st.error(f"Backend unavailable: {error}")
        return

    documents = load_documents()
    render_admin_header(health)
    render_admin_metrics(health)

    upload_tab, library_tab = st.tabs(["Upload", "Library"])
    with upload_tab:
        render_upload_panel()
    with library_tab:
        render_document_library(documents)

apply_theme()
init_state()
render_sidebar()

if st.session_state.active_page == "Admin":
    render_admin_page()
else:
    render_chatbot_page()
