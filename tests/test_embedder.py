from src.embedder import Embedder


embedder = Embedder()

vector = embedder.embed(
    "Retrieval augmented generation improves language model answers."
)

print("Embedding type:", type(vector))
print("Embedding shape:", vector.shape)
print("First 5 values:", vector[:5])