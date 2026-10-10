
import json

from src.rag_pipeline import RAGPipeline
from src.evaluator import evaluate_retrieval

with open("eval/questions.json", encoding="utf-8") as file:
    test_cases = json.load(file)

pipeline = RAGPipeline()

evaluate_retrieval(
    pipeline,
    test_cases,
    k=3
)
