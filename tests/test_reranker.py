from src.pdf_loader import load_pdf
from src.chunker import chunk_document
from src.embedder import Embedder
from src.vector_store import VectorStore
from src.lexical_retriever import LexicalRetriever
from src.hybrid_retriever import HybridRetriever
from src.reranker import Reranker


document = load_pdf("data/raw/python.pdf")
chunks = chunk_document(document)

embedder = Embedder()
store = VectorStore()

for chunk in chunks:
    vector = embedder.embed(chunk.text)
    store.add(chunk, vector, document)


class SemanticRetriever:

    def __init__(self, store, chunks):
        self.store = store
        self.chunks = chunks

    def search(self, query_vector, top_k=10):
        results = self.store.search(query_vector, top_k)

        lookup = {chunk.id: chunk for chunk in self.chunks}

        return [
            (1 / (i + 1), lookup[chunk_id])
            for i, chunk_id in enumerate(results["ids"][0])
        ]


semantic = SemanticRetriever(store, chunks)
lexical = LexicalRetriever(chunks)

hybrid = HybridRetriever(
    semantic,
    lexical
)

query = "What libraries are used for data science?"

query_vector = embedder.embed(query)

candidates = hybrid.search(
    query,
    query_vector,
    top_k=10
)

candidate_chunks = [
    chunk for _, chunk in candidates
]


reranker = Reranker()

final_results = reranker.rerank(
    query,
    candidate_chunks,
    top_k=3
)


for score, chunk in final_results:
    print("\nReranker score:", score)
    print("Chunk:", chunk.id)
    print(chunk.text[:500])