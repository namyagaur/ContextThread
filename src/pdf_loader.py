import os
from pypdf import PdfReader

from src.document import Document
from src.cleaner import clean_text

def load_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        pages = []
        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        content = "\n\n".join(pages)
        content = clean_text(content)

        filename = os.path.basename(file_path)

        d = Document(
            id= filename,
            title=filename,
            content=content,
            source=file_path,
            date="unknown"
        )
        return d
    except FileNotFoundError:
        print(f"File not found:{file_path}")
        return None