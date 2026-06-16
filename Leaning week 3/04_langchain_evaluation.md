# Day 6-7 - LangChain & Evaluation

## Muc tieu

Hieu vai tro cua LangChain va cach danh gia chat luong RAG chatbot.

## 1. LangChain

### Dinh nghia

LangChain la framework giup noi cac buoc LLM app: prompt, model, retriever, chain, memory, tool.

### Vi du concept

```text
Retriever -> Prompt Template -> LLM -> Output Parser
```

## 2. Chain

### Dinh nghia

Chain la chuoi cac buoc xu ly duoc noi voi nhau. Trong RAG, chain thuong gom retriever + prompt + LLM.

### Pseudo-code

```python
def rag_chain(question):
    docs = retriever.get_relevant_documents(question)
    prompt = build_prompt(docs, question)
    answer = llm.generate(prompt)
    return answer
```

## 3. Reranking

### Dinh nghia

Reranking sap xep lai ket qua retrieval bang model/logic tot hon. Retrieval dau tien lay top 20, reranker chon top 5 tot nhat.

### Vi du

```text
Vector search top 20 -> reranker -> final top 5 context
```

## 4. Metadata Filtering

### Dinh nghia

Metadata filtering gioi han search theo source, page, document type, date, project.

### Vi du

```python
filters = {"source": "week2", "page": 1}
```

## 5. RAG Evaluation

### Dinh nghia

RAG evaluation do chatbot co retrieve dung context va tra loi dung khong.

### Metrics co ban

| Metric | Y nghia |
| --- | --- |
| Context relevance | Context retrieve co lien quan question khong |
| Answer faithfulness | Answer co dua tren context khong |
| Answer correctness | Answer co dung khong |
| Citation quality | Source co dung khong |

## 6. RAGAS

### Dinh nghia

RAGAS la toolkit danh gia RAG. No co metrics nhu faithfulness, answer relevancy, context precision, context recall.

### Vi du concept

```text
question + answer + contexts + ground_truth -> metrics
```

## Bai tap

Tao file:

```text
day6_rag_evaluation.md
```

Yeu cau:

- Tao 5 cau hoi test.
- Ghi expected source cho moi cau.
- Chay retrieval.
- Check retrieved source co dung expected source khong.
- Ghi diem pass/fail.

## Checklist

- Hieu LangChain dung de noi pipeline.
- Biet chain la gi.
- Biet reranking giai quyet van de gi.
- Biet metadata filtering dung khi nao.
- Danh gia duoc RAG bang test questions.

