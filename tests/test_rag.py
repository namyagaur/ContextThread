from src.rag_pipeline import RAGPipeline

pipeline = RAGPipeline("data/raw/python.pdf")

result = pipeline.answer(
    "What libraries are used for data science?"
)

print("\nANSWER:")
print(result["answer"])

print("\nSOURCES:")
for source in result["sources"]:
    print(source["chunk_id"])
    print(source["text"][:200])