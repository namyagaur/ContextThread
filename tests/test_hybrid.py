from src.pdf_loader import load_pdf
from src.chunker import chunk_document
from src.embedder import Embedder
from src.vector_store import VectorStore
from src.lexical_retriever import LexicalRetriever
from src.hybrid_retriever import HybridRetriever


document = load_pdf("data/raw/python.pdf")
chunks = chunk_document(document)

embedder = Embedder()

store = VectorStore()

for chunk in chunks:
    vector = embedder.embed(chunk.text)
    store.add(chunk, vector, document)


class SemanticRetriever:

    def __init__(self, store):
        self.store = store

    def search(self, query_vector, top_k=5):
        results = self.store.search(query_vector, top_k)

        output = []

        for i, chunk_id in enumerate(results["ids"][0]):
            chunk = next(c for c in chunks if c.id == chunk_id)
            output.append((1 / (i + 1), chunk))

        return output


semantic = SemanticRetriever(store)
lexical = LexicalRetriever(chunks)

hybrid = HybridRetriever(semantic, lexical)


query = "What libraries are used for data science?"

query_vector = embedder.embed(query)

results = hybrid.search(
    query,
    query_vector,
    top_k=3
)

for score, chunk in results:
    print("\nRRF Score:", score)
    print(chunk.text[:400])