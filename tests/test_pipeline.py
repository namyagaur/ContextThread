from src.rag_pipeline import RAGPipeline


pipeline = RAGPipeline(
    "data/raw/python.pdf"
)

query = "What libraries are used for data science?"

results, context = pipeline.retrieve(query)

print("\n========== RETRIEVED EVIDENCE ==========")

for score, chunk in results:
    print(f"\nScore: {score}")
    print(f"Chunk: {chunk.id}")
    print(chunk.text[:300])

print("\n========== CONTEXT FOR LLM ==========")
print(context)