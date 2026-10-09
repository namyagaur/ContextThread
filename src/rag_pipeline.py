from src.pdf_loader import load_pdf
from src.chunker import chunk_document
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

    def search(self, query_vector, top_k=10):
        results = self.store.search(query_vector, top_k)

        lookup = {
            chunk.id: chunk
            for chunk in self.chunks
        }

        return [
            (1 / (i + 1), lookup[chunk_id])
            for i, chunk_id in enumerate(results["ids"][0])
        ]



class RAGPipeline:

    def __init__(self, document_path):
        self.document = load_pdf(document_path)
        self.chunks = chunk_document(self.document)

        self.embedder = Embedder()
        self.store = VectorStore()

        semantic = SemanticRetriever(self.store, self.chunks)
        lexical = LexicalRetriever(self.chunks)

        self.hybrid = HybridRetriever(semantic, lexical)
        self.reranker = Reranker()
        self.context_builder = ContextBuilder()
        self.generator = Generator()

    def retrieve(self, query):
        query_vector = self.embedder.embed(query)

        candidates = self.hybrid.search(
            query,
            query_vector,
            top_k=10
        )

        candidate_chunks = [
            chunk for _, chunk in candidates
        ]

        reranked = self.reranker.rerank(
            query,
            candidate_chunks,
            top_k=3
        )

        context = self.context_builder.build(reranked)

        return reranked, context

    def answer(self, query):
        results, context = self.retrieve(query)

        response = self.generator.generate(query, context)

        return {
            "answer": response,
            "sources": [
                {
                    "chunk_id": chunk.id,
                    "score": float(score),
                    "text": chunk.text
                }
                for score, chunk in results
            ]
        }
