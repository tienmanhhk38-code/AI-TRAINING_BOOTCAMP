import json
from pathlib import Path

from evaluator import evaluate_answer
from generator import generate_answer
from retriever import retrieve_context
from vector_store import VectorStore


QUESTIONS = [
    "What does Week 3 focus on?",
    "What should learners build in Week 4?",
    "Which week teaches OCR?",
    "What Python skills are learned in Week 1?",
]


def load_chunks(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def export_answers(records, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)


def build_vector_store(chunks):
    vector_store = VectorStore()
    vector_store.add_documents(chunks)
    return vector_store


def answer_questions(questions, vector_store):
    records = []

    for question in questions:
        contexts = retrieve_context(question, vector_store, top_k=2)
        generated = generate_answer(question, contexts)
        record = {
            "question": question,
            "answer": generated["answer"],
            "sources": generated["sources"],
            "contexts": contexts,
        }
        record["evaluation"] = evaluate_answer(record)
        records.append(record)

    return records


def main():
    project_dir = Path(__file__).resolve().parent.parent
    input_path = project_dir / "input" / "chunks.json"
    output_path = project_dir / "output" / "answers.json"

    chunks = load_chunks(input_path)
    vector_store = build_vector_store(chunks)
    records = answer_questions(QUESTIONS, vector_store)
    export_answers(records, output_path)

    print(f"Loaded chunks: {len(chunks)}")
    print(f"Answered questions: {len(records)}")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
