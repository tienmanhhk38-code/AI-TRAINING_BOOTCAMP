def evaluate_answer(answer_record):
    answer = answer_record["answer"]
    contexts = answer_record["contexts"]
    sources = answer_record["sources"]

    return {
        "has_context": bool(contexts),
        "has_sources": bool(sources),
        "answer_length": len(answer),
        "top_score": contexts[0]["score"] if contexts else 0,
    }
