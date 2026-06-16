from embeddings import cosine_similarity, embed_text


class VectorStore:
    def __init__(self):
        self.items = []

    def add_documents(self, chunks):
        for chunk in chunks:
            self.items.append({
                "chunk": chunk,
                "embedding": embed_text(chunk["text"]),
            })

    def search(self, query, top_k=3):
        query_embedding = embed_text(query)
        scored_items = []

        for item in self.items:
            score = cosine_similarity(query_embedding, item["embedding"])
            scored_items.append({
                "score": score,
                "chunk": item["chunk"],
            })

        scored_items.sort(key=lambda item: item["score"], reverse=True)
        return [item for item in scored_items[:top_k] if item["score"] > 0]
