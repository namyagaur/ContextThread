from src.loader import load_text_file


document = load_text_file("data/raw/does_not_exist.txt")
print(document)
print(document.id)
print(document.title)
print(document.content)
print(document.source)
print(document.date)