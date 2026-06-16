# Day 3-4 - Streamlit Chat UI

## Muc tieu

Xay UI chat local de upload file, hoi dap, hien citations va conversation history.

## 1. Streamlit

### Dinh nghia

Streamlit la framework Python tao UI nhanh cho data/AI app.

### Vi du

```python
import streamlit as st

st.title("AI Chatbot")
question = st.chat_input("Ask a question")
```

## 2. Chat Input

### Dinh nghia

Chat input la o nhap cau hoi cua user. Khi user submit, frontend goi backend `/ask`.

### Vi du

```python
question = st.chat_input("Ask from uploaded document")
if question:
    st.write(question)
```

## 3. Citations Display

### Dinh nghia

Citations la danh sach source/chunk backend da dung de tra loi. UI can hien citation de user kiem chung.

### Vi du

```python
sources = ["week4:c1", "week3:c2"]
st.caption("Sources: " + ", ".join(sources))
```

## 4. Conversation History

### Dinh nghia

Conversation history la danh sach message user/assistant trong session.

### Vi du

```python
if "messages" not in st.session_state:
    st.session_state.messages = []

st.session_state.messages.append({"role": "user", "content": question})
```

## 5. Frontend to Backend

### Dinh nghia

Frontend goi backend qua HTTP. Streamlit app co the dung `requests`.

### Vi du

```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/ask",
    json={"question": question},
    timeout=30,
)
data = response.json()
```

## Bai tap

Tao `frontend/app.py`:

- Upload file.
- Hien chat history.
- Goi `/ask`.
- Hien answer.
- Hien citations.

## Checklist

- Chay duoc Streamlit app.
- Upload file tu UI.
- Gui question len backend.
- Hien answer.
- Hien sources/citations.

