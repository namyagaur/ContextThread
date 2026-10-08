from src.pdf_loader import load_pdf
from src.chunker import chunk_text


document = load_pdf("data/raw/python.pdf")

chunks = chunk_text(document.content)

print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks[:3]):
    print(f"\n--- CHUNK {i} ---")
    print(chunk)