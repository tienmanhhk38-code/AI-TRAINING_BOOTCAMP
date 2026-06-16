# Week 3 - LLM & RAG System

Nguon lo trinh: `../README.md`

Muc tieu Week 3: xay RAG chatbot co the tra loi cau hoi tu tai lieu that.

Flow can nam:

```text
Question -> Embed Query -> Retrieve Context -> Build Prompt -> Generate Answer -> Cite Sources
```

## Danh sach bai hoc

| Ngay | File | Noi dung |
| --- | --- | --- |
| Day 1-2 | [01_llm_prompt_engineering.md](01_llm_prompt_engineering.md) | LLM, Gemini/Groq API, system prompt, few-shot |
| Day 3 | [02_embeddings_vector_db.md](02_embeddings_vector_db.md) | Embeddings, vector DB, cosine similarity |
| Day 4-5 | [03_rag_pipeline.md](03_rag_pipeline.md) | Chunking, indexing, retrieval, generation |
| Day 6-7 | [04_langchain_evaluation.md](04_langchain_evaluation.md) | LangChain, reranking, metadata filtering, RAG evaluation |
| Project | [05_rag_chatbot_project.md](05_rag_chatbot_project.md) | Mini project RAG chatbot local |

## Cach hoc moi ngay

1. Doc dinh nghia.
2. Chay vi du nho.
3. So sanh query, context, answer.
4. Lam bai tap.
5. Tick checklist.

## Deliverable cuoi tuan

Project dau ra da tao o `../week3_project/`.

```text
week3_project/
  input/
    chunks.json
  output/
    answers.json
  src/
    main.py
    embeddings.py
    vector_store.py
    retriever.py
    generator.py
    evaluator.py
```

Chay project:

```powershell
cd ../week3_project
python src/main.py
```

Tieu chi dat:

- Doc chunks tu `input/chunks.json`.
- Embed query va chunks.
- Retrieve context lien quan bang cosine similarity.
- Generate answer dua tren context.
- Ghi ket qua ra `output/answers.json`.
- Co citations/source metadata.
- Chay local khong can API key.

