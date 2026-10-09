
from src.pdf_loader import load_pdf
from src.chunker import chunk_document

document = load_pdf("data/raw/python.pdf")
chunks = chunk_document(document)

print("Document:", document.title)
print("PDF pages:", len(document.pages))
print("Total chunks:", len(chunks))

for chunk in chunks:
    print(
        f"\nID: {chunk.id}"
        f"\nPage: {chunk.page_number}"
        f"\nLength: {len(chunk.text)}"
        f"\nText: {chunk.text[:150]}"
    )

assert chunks, "No chunks were generated"
assert all(len(c.text) >= 40 for c in chunks)
assert all(c.page_number is not None for c in chunks)
