
import chromadb
from src.chunk import Chunk

class VectorStore:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="data/chroma"
        )

        self.collection = self.client.get_or_create_collection(
            name="contextthread"
        )

    def add(self, chunk, vector, document):
        self.collection.upsert(
            ids=[chunk.id],
            embeddings=[vector.tolist()],
            documents=[chunk.text],
            metadatas=[{
                "document_id": chunk.document_id,
                "chunk_index": chunk.index,
                "source": document.source,
                "title": document.title,
                "date": document.date,
                "page_number": chunk.page_number or 0
            }]
        )

    def search(self, query_vector, top_k=5, where=None):
        return self.collection.query(
            query_embeddings=[query_vector.tolist()],
            n_results=top_k,
            where=where,
            include=["documents", "metadatas", "distances"]
        )

    def delete_document(self, document_id):
        self.collection.delete(
            where={"document_id": document_id}
        )

    

    def get_all_chunks(self):
        records = self.collection.get(
            include=["documents", "metadatas"]
        )

        chunks = []

        for i, chunk_id in enumerate(records["ids"]):
            metadata = records["metadatas"][i] or {}

            chunks.append(
                Chunk(
                    id=chunk_id,
                    document_id=metadata["document_id"],
                    index=metadata["chunk_index"],
                    text=records["documents"][i],
                    page_number=metadata.get("page_number") or None
                )
            )

        return chunks
