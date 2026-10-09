from src.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()

result = pipeline.answer(
    "What libraries are used for data science?"
)

print("\nANSWER:")
print(result["answer"])

print("\nCITATION SOURCES:")
for i, source in enumerate(result["sources"], start=1):
    print(f"\n[SOURCE {i}]")
    print("Chunk:", source["chunk_id"])
    print("Document:", source["document_id"])
    print("Page:", source["page_number"])
    print("Evidence:", source["text"][:200])