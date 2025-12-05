from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from app.court.graph import court_graph
from app.db.session import get_db
from app.db.models.case import Case
from app.services.memory import store_case_memory

router = APIRouter()

class CaseRequest(BaseModel):
    query: str
    image_url: Optional[str] = None

@router.post("/submit")
async def submit_case(request: CaseRequest, db: Session = Depends(get_db)):
    print(f"New Case Received: {request.query}")
    
    clean_image_url = request.image_url
    if clean_image_url and (clean_image_url.strip() == "" or clean_image_url == "string"):
        clean_image_url = None

    if clean_image_url:
        print(f"Visual Evidence Included: {clean_image_url}")

    db_case = Case(query=request.query, status="processing")
    db.add(db_case)
    db.commit()
    db.refresh(db_case)

    initial_state = {
        "original_query": request.query,
        "image_url": clean_image_url,
        "revision_count": 0,
        "relevant_context": "" 
    }
    
    try:
        final_state = await court_graph.ainvoke(initial_state)
        
        db_case.verdict = final_state.get("verdict")
        db_case.solution = final_state.get("proposed_solution")
        db_case.status = "closed"
        db.commit()
        if final_state.get("proposed_solution"):
            memory_text = f"Query: {request.query}\nSolution: {final_state.get('proposed_solution')}"
            store_case_memory(db, db_case.id, memory_text)
        
        return {
            "verdict": final_state.get("verdict"),
            "final_solution": final_state.get("proposed_solution"),
            "rounds": final_state.get("revision_count", 0)
        }
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))