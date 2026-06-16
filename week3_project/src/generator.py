def generate_answer(question, contexts):
    if not contexts:
        return {
            "answer": "I do not know from the provided context.",
            "sources": [],
        }

    best_context = contexts[0]
    answer = (
        f"Based on the retrieved context, {best_context['text']} "
        f"This answers the question: {question}"
    )

    return {
        "answer": answer,
        "sources": [context["chunk_id"] for context in contexts],
    }
