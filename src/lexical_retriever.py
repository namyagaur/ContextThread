
import re
from rank_bm25 import BM25Okapi


def tokenize(text):
    return re.findall(r"\b[a-zA-Z0-9_+#.-]+\b", text.lower())


class LexicalRetriever:

    def __init__(self, chunks):
        self.chunks = chunks

        tokenized_chunks = [
            tokenize(chunk.text)
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(tokenized_chunks)

    def search(self, query, top_k=5):
        query_tokens = tokenize(query)
        scores = self.bm25.get_scores(query_tokens)

        ranked = sorted(
            zip(scores, self.chunks),
            key=lambda item: item[0],
            reverse=True
        )

        return ranked[:top_k]
