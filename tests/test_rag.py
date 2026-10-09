
from src.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()

result = pipeline.answer(
    "What libraries are used for data science?"
)

print("\nANSWER:")
print(result["answer"])

print("\nSOURCES:")
for source in result["sources"]:
    print("Chunk:", source["chunk_id"])
    print("File:", source["source"])
    print("Page:", source["page_number"])
    print(source["text"][:200])
    print()
