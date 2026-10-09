
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.chunk import Chunk


class DocumentChunker:

    def __init__(self, chunk_size=800, overlap=120):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
            add_start_index=True
        )

    def chunk_document(self, document):
        chunks = []
        global_index = 0

        # Preserve page numbers for PDFs.
        if document.pages:
            page_contents = enumerate(document.pages, start=1)
        else:
            page_contents = [(None, document.content)]

        for page_number, page_text in page_contents:
            if not page_text.strip():
                continue

            split_docs = self.splitter.create_documents(
                [page_text]
            )

            for split_doc in split_docs:
                text = split_doc.page_content.strip()

                # Discard tiny, usually unhelpful fragments.
                if len(text) < 40:
                    continue

                chunks.append(
                    Chunk(
                        id=f"{document.id}_chunk_{global_index}",
                        document_id=document.id,
                        index=global_index,
                        text=text,
                        page_number=page_number
                    )
                )

                global_index += 1

        return chunks


def chunk_document(document, chunk_size=800, overlap=120):
    chunker = DocumentChunker(chunk_size, overlap)
    return chunker.chunk_document(document)
