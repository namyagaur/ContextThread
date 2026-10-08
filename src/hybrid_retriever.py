class HybridRetriever:

    def __init__(self, semantic_retriever, lexical_retriever):
        self.semantic_retriever = semantic_retriever
        self.lexical_retriever = lexical_retriever

    def search(self, query, query_vector, top_k=5):
        semantic_results = self.semantic_retriever.search(
            query_vector,
            top_k=top_k
        )

        lexical_results = self.lexical_retriever.search(
            query,
            top_k=top_k
        )

        scores = {}

        for rank, (score, chunk) in enumerate(semantic_results):
            scores[chunk.id] = scores.get(chunk.id, 0) + 1 / (60 + rank + 1)

        for rank, (score, chunk) in enumerate(lexical_results):
            scores[chunk.id] = scores.get(chunk.id, 0) + 1 / (60 + rank + 1)

        chunk_lookup = {}

        for _, chunk in semantic_results:
            chunk_lookup[chunk.id] = chunk

        for _, chunk in lexical_results:
            chunk_lookup[chunk.id] = chunk

        ranked = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            (score, chunk_lookup[chunk_id])
            for chunk_id, score in ranked[:top_k]
        ]