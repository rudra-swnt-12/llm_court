from app.court.state import CaseFile
from app.db.session import SessionLocal
from app.services.memory import search_similar_cases

def recall_precedents(state: CaseFile):
    """
    Role: The Archivist
    Task: Check if we have solved a similar problem before.
    """
    print("ARCHIVIST: Searching legal archives...")
    
    query = state["original_query"]
    
    db = SessionLocal()
    try:
        past_cases = search_similar_cases(db, query)
    finally:
        db.close()
    
    if not past_cases:
        print("ARCHIVIST: No precedent found.")
        return {"relevant_context": "No prior cases found."}

    context_text = "Here are relevant past rulings to guide you:\n"
    for case in past_cases:
        snippet = case.solution[:500] if case.solution else "No solution recorded."
        context_text += f"- PRECEDENT QUERY: {case.query}\n  VERDICT: {case.verdict}\n  APPROVED CODE SNIPPET: {snippet}...\n\n"
        
    print(f"ARCHIVIST: Found {len(past_cases)} precedents.")
    return {"relevant_context": context_text}