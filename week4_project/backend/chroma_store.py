import hashlib

from backend.search_utils import tokenize


def dense_embedding(text, dimensions=384):
    vector = [0.0] * dimensions

    for token in tokenize(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dimensions
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[index] += sign

    norm = sum(value * value for value in vector) ** 0.5
    if norm == 0:
        return vector

    return [value / norm for value in vector]


class ChromaStore:
    def __init__(self, path, collection_name="week4_documents"):
        import chromadb

        self.path = str(path)
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path=self.path)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def reset(self, chunks):
        try:
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        self.upsert(chunks)

    def upsert(self, chunks):
        if not chunks:
            return

        seen_ids = {}
        ids = []
        for chunk in chunks:
            base_id = chunk["chunk_id"]
            seen_ids[base_id] = seen_ids.get(base_id, 0) + 1
            ids.append(base_id if seen_ids[base_id] == 1 else f"{base_id}#{seen_ids[base_id]}")

        documents = [chunk.get("text", "") for chunk in chunks]
        metadatas = [
            {
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk.get("document_id") or "",
                "source": chunk.get("source", ""),
            }
            for chunk in chunks
        ]
        embeddings = [dense_embedding(document) for document in documents]

        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def query(self, question, top_k=3):
        result = self.collection.query(
            query_embeddings=[dense_embedding(question)],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]

        contexts = []
        for document, metadata, distance in zip(documents, metadatas, distances):
            score = max(0.0, 1.0 - float(distance))
            contexts.append({
                "chunk_id": metadata.get("chunk_id", ""),
                "document_id": metadata.get("document_id", ""),
                "source": metadata.get("source", ""),
                "text": document,
                "score": round(score, 4),
            })

        return contexts

    def close(self):
        close_client = getattr(self.client, "close", None)
        if close_client:
            close_client()
