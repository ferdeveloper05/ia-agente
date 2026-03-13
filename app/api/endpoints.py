from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from services.agent_service import agente_executor

router = APIRouter()

class Query(BaseModel):
    session_id: str
    question: str

@router.post("/ask")
def ask(query: Query):
    try:
        answer = agente_executor(query.session_id, query.question)
        return {"response": answer, "session_id": query.session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
