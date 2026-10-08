from src.pdf_loader import load_pdf
from src.chunker import chunk_document
from src.embedder import Embedder
from src.vector_store import VectorStore


document = load_pdf("data/raw/python.pdf")

chunks = chunk_document(document)

embedder = Embedder()
store = VectorStore()

for chunk in chunks:
    vector = embedder.embed(chunk.text)
    store.add(chunk, vector, document)

print(f"Indexed {len(chunks)} chunks.")


query = "What can Python be used for?"

query_vector = embedder.embed(query)

results = store.search(
    query_vector,
    top_k=3,
    where={"date": "unknown"}
)

print("\nRESULTS")

for i, document in enumerate(results["documents"][0]):
    print(f"\n--- Result {i + 1} ---")
    print(document[:500])