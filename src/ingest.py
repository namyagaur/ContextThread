
from src.pdf_loader import load_pdf
from src.chunker import chunk_document
from src.embedder import Embedder
from src.vector_store import VectorStore


def ingest_pdf(file_path):
    document = load_pdf(file_path)

    if document is None:
        raise FileNotFoundError(file_path)

    chunks = chunk_document(document)
    embedder = Embedder()
    store = VectorStore()

    for chunk in chunks:
        vector = embedder.embed(chunk.text)
        store.add(chunk, vector, document)

    print(f"Document: {document.title}")
    print(f"Chunks indexed: {len(chunks)}")

    return chunks
