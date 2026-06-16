def retrieve_context(question, vector_store, top_k=3):
    matches = vector_store.search(question, top_k=top_k)

    return [
        {
            "chunk_id": match["chunk"]["chunk_id"],
            "source": match["chunk"]["source"],
            "text": match["chunk"]["text"],
            "score": round(match["score"], 4),
        }
        for match in matches
    ]
