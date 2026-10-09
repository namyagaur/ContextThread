
import os
from pypdf import PdfReader

from src.document import Document
from src.cleaner import clean_text


def load_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        pages = []

        for page in reader.pages:
            text = page.extract_text() or ""
            pages.append(clean_text(text))

        content = "\n\n".join(
            text for text in pages if text
        )

        filename = os.path.basename(file_path)

        return Document(
            id=filename,
            title=filename,
            content=content,
            source=file_path,
            date="unknown",
            pages=pages
        )

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
