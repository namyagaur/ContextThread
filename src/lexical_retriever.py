from rank_bm25 import BM25Okapi


class LexicalRetriever:

    def __init__(self, chunks):
        self.chunks = chunks

        tokenized_chunks = [
            chunk.text.lower().split()
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(tokenized_chunks)

    def search(self, query, top_k=5):
        query_tokens = query.lower().split()

        scores = self.bm25.get_scores(query_tokens)

        ranked = sorted(
            zip(scores, self.chunks),
            key=lambda x: x[0],
            reverse=True
        )

        return ranked[:top_k]