
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.rag_pipeline import RAGPipeline

app = FastAPI(
    title="ContextThread API",
    description="Research retrieval and grounded question answering",
    version="0.1.0"
)

pipeline = None


class QueryRequest(BaseModel):
    query: str = Field(min_length=3, max_length=2000)


@app.on_event("startup")
def load_pipeline():
    global pipeline
    pipeline = RAGPipeline()


@app.get("/health")
def health():
    return {"status": "ok", "service": "ContextThread"}


@app.post("/query")
def query_knowledge_base(request: QueryRequest):
    try:
        result = pipeline.answer(request.query)
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Query processing failed. Check server logs."
        ) from exc
