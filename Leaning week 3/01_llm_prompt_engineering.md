# Day 1-2 - LLM & Prompt Engineering

## Muc tieu

Hieu LLM la gi, prompt gom nhung phan nao, va biet cach goi LLM API o muc co ban.

## 1. LLM

### Dinh nghia

LLM la Large Language Model. No nhan input text va sinh output text. Trong chatbot, LLM tao cau tra loi dua tren question va context.

### Vi du

```text
Question: Week 3 hoc gi?
LLM Answer: Week 3 hoc LLM, embeddings, vector DB va RAG pipeline.
```

## 2. Prompt

### Dinh nghia

Prompt la noi dung gui vao LLM. Prompt tot phai ro vai tro, task, context, format output.

### Vi du

```text
You are an AI training assistant.
Use only the provided context.
If the answer is not in context, say "I do not know".

Context:
Week 3 focuses on LLM and RAG.

Question:
What does Week 3 focus on?
```

## 3. System Prompt

### Dinh nghia

System prompt dat quy tac chung cho LLM: vai tro, gioi han, cach tra loi.

### Vi du

```python
system_prompt = """
You are a document Q&A assistant.
Answer only from provided context.
Include source names when possible.
"""
```

## 4. Few-shot Prompt

### Dinh nghia

Few-shot prompt dua mot vai vi du question/answer de LLM hoc format tra loi mong muon.

### Vi du

```text
Example:
Q: What is Week 2 about?
A: Week 2 is about AI Architecture and OCR. Source: week2.

Q: What is Week 3 about?
A:
```

## 5. Chain-of-thought

### Dinh nghia

Chain-of-thought la cach yeu cau model suy luan tung buoc. Trong app production, khong nen hien reasoning noi bo; nen yeu cau model tra loi ngan gon va dua evidence.

### Vi du an toan

```text
Think through the context privately, then answer with:
- Answer
- Sources
```

## 6. Gemini/Groq API

### Dinh nghia

Gemini va Groq la LLM API providers. Code that can API key trong `.env`, khong hardcode key.

### Pseudo-code

```python
import os

api_key = os.getenv("GEMINI_API_KEY")
prompt = "Answer from context..."

# client.generate(prompt)
```

## Bai tap

Tao file:

```text
day1_prompt_engineering.md
```

Yeu cau:

- Viet system prompt cho document Q&A.
- Viet prompt template co `context` va `question`.
- Viet 2 few-shot examples.
- Dinh nghia output format: answer + sources.

## Checklist

- Giai thich duoc LLM la gi.
- Phan biet system prompt va user prompt.
- Viet duoc prompt dua tren context.
- Biet API key phai nam trong `.env`.
- Biet khong tra loi ngoai context trong RAG.

