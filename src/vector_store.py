import chromadb


class VectorStore:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="data/chroma"
        )

        self.collection = self.client.get_or_create_collection(
            name="contextthread"
        )

    def add(self, chunk, vector):
        self.collection.add(
            ids=[chunk.id],
            embeddings=[vector.tolist()],
            documents=[chunk.text],
            metadatas=[{
                "document_id": chunk.document_id,
                "chunk_index": chunk.index
            }]
        )

    def search(self, query_vector, top_k=5):
        return self.collection.query(
            query_embeddings=[query_vector.tolist()],
            n_results=top_k
        )