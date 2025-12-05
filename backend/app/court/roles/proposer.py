from app.court.state import CaseFile
from app.services.llm import get_llm
from app.core.config import settings

# Uses GPT-OSS-20B as the Defense model
llm = get_llm(settings.MODEL_DEFENSE, temperature=0.7)

def draft_solution(state: CaseFile):
    """The Builder"""
    print("DEFENSE: Drafting solution...")
    
    query = state["original_query"]
    critique = state.get("prosecutor_critique", None)
    
    if critique:
        prompt = f"Fix this solution based on critique: {critique}\n\nOriginal Request: {query}"
    else:
        prompt = f"Write a solution for: {query}"

    response = llm.invoke(prompt)
    
    return {
        "proposed_solution": response.content,
        "revision_count": state.get("revision_count", 0) + 1
    }