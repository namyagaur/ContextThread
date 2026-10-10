
from pathlib import Path

from src.ingest import ingest_pdf


def ingest_directory(directory="data/raw"):
    pdf_files = sorted(Path(directory).glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in {directory}"
        )

    for pdf_path in pdf_files:
        print(f"\nIngesting: {pdf_path.name}")
        ingest_pdf(str(pdf_path))


if __name__ == "__main__":
    ingest_directory()
