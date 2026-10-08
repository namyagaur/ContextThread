from src.pdf_loader import load_pdf
from src.chunker import chunk_document
from src.lexical_retriever import LexicalRetriever


document = load_pdf("data/raw/python.pdf")

chunks = chunk_document(document)

retriever = LexicalRetriever(chunks)

results = retriever.search(
    "Python Pandas NumPy",
    top_k=3
)

for score, chunk in results:
    print("\nScore:", score)
    print(chunk.text[:400])