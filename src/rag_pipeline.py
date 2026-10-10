import re
from src.embedder import Embedder
from src.vector_store import VectorStore
from src.lexical_retriever import LexicalRetriever
from src.hybrid_retriever import HybridRetriever
from src.reranker import Reranker
from src.context_builder import ContextBuilder
from src.generator import Generator


class SemanticRetriever:

    def __init__(self, store, chunks):
        self.store = store
        self.chunks = chunks
        self.lookup = {chunk.id: chunk for chunk in chunks}

    def search(self, query_vector, top_k=10):
        results = self.store.search(query_vector, top_k)

        ranked = []

        for rank, chunk_id in enumerate(results["ids"][0]):
            chunk = self.lookup.get(chunk_id)

            if chunk is not None:
                ranked.append((1 / (rank + 1), chunk))

        return ranked


class RAGPipeline:

    def __init__(self):
        self.embedder = Embedder()
        self.store = VectorStore()

        # Load the existing index; do not re-ingest the PDF.
        self.chunks = self.store.get_all_chunks()

        if not self.chunks:
            raise RuntimeError(
                "Knowledge base is empty. Run ingestion first."
            )

        semantic = SemanticRetriever(
            self.store, self.chunks
        )
        lexical = LexicalRetriever(self.chunks)

        self.hybrid = HybridRetriever(semantic, lexical)
        self.reranker = Reranker()
        self.context_builder = ContextBuilder()
        self.generator = Generator()

    def retrieve(self, query):
        query_vector = self.embedder.embed(query)

        candidates = self.hybrid.search(
            query, query_vector, top_k=10
        )

        candidate_chunks = [
            chunk for _, chunk in candidates
        ]

        reranked = self.reranker.rerank(
            query, candidate_chunks, top_k=3
        )

        context, source_map = self.context_builder.build(reranked)
        return reranked, context, source_map


    def answer(self, query):
        results, context, source_map = self.retrieve(query)
        response = self.generator.generate(query, context)

        cited_labels = set(
            re.findall(r"\[SOURCE \d+\]", response)
        )

        valid_labels = {
            f"[{label}]" for label in source_map
        }

        invalid_labels = cited_labels - valid_labels

        if invalid_labels:
            raise ValueError(
                f"Invalid citation labels: {invalid_labels}"
            )

        return {
            "answer": response,
            "sources": [
                {"label": label, **source}
                for label, source in source_map.items()
            ]
        }



    def _source_for(self, chunk):
        records = self.store.collection.get(
            ids=[chunk.id],
            include=["metadatas"]
        )

        if records["metadatas"]:
            return records["metadatas"][0].get("source")

        return None
