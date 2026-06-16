# Week 3 Project - Local RAG Chatbot

Project dau ra Week 3: doc chunks, retrieve context lien quan, generate answer local, va ghi citations.

Ban mau chay local khong can API key. Muc tieu la hieu RAG flow truoc khi doi sang Gemini/Groq, ChromaDB/FAISS, LangChain.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

```powershell
python src/main.py
```

## Input

```text
input/chunks.json
```

## Output

```text
output/answers.json
```

## Flow

```text
chunks.json -> embed chunks -> embed question -> retrieve top-k -> generate answer -> evaluate -> answers.json
```

