from fastapi import APIRouter

from src.API.schemas import QueryRequest,QueryResponse
from src.Rag.generator import Generator

router = APIRouter(prefix="/rag",tags=["RAG"])
generator = Generator()

@router.post("/query",response_model=QueryResponse)
def query_rag(request: QueryRequest):
    obj = generator.generate_answer(request.question)
    return QueryResponse(answer=obj["answer"],sources=obj["sources"])