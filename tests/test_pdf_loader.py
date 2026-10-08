from src.pdf_loader import load_pdf


document = load_pdf("data/raw/python.pdf")

print("ID:", document.id)
print("TITLE:", document.title)
print("SOURCE:", document.source)
print("CONTENT PREVIEW:")
print(document.content[:2000])