from src.pdf_loader import load_pdf
from src.chunker import chunk_document


document = load_pdf("data/raw/python.pdf")

chunks = chunk_document(document)

print("Number of chunks:", len(chunks))

for chunk in chunks[:3]:
    print(f"\n--- {chunk.id} ---")
    print("Document:", chunk.document_id)
    print("Index:", chunk.index)
    print(chunk.text)