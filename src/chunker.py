from src.chunk import Chunk


def chunk_document(document, chunk_size=500, overlap=50):
    chunks = []

    start = 0
    index = 0

    while start < len(document.content):
        end = start + chunk_size

        text = document.content[start:end]

        chunk = Chunk(
            id=f"{document.id}_chunk_{index}",
            document_id=document.id,
            index=index,
            text=text
        )

        chunks.append(chunk)

        index += 1
        start = end - overlap

    return chunks