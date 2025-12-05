from app.court.state import CaseFile
from app.services.llm import get_llm
from app.core.config import settings

# Uses Llama 3.3 70B as the Prosecutor model
llm = get_llm(settings.MODEL_PROSECUTOR, temperature=0.8)

def cross_examine(state: CaseFile):
    """The Attack"""
    print("PROSECUTOR: Cross-examining...")
    
    solution = state.get("proposed_solution", "")
    query = state["original_query"]
    
    prompt = f"""
    You are the Chief Prosecutor. 
    User Query: {query}
    Defense Solution: {solution}
    
    Identify 3 flaws (Security, Performance, or Logic).
    If the code is dangerous, reject it immediately.
    """
    
    response = llm.invoke(prompt)
    return {"prosecutor_critique": response.content}