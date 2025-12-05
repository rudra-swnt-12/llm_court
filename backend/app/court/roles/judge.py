from app.court.state import CaseFile
from app.services.llm import get_llm
from app.core.config import settings
from pydantic import BaseModel, Field

# Uses GPT-OSS-120B as the Judge model
llm = get_llm(settings.MODEL_JUDGE, temperature=0.1)

class JudicialRuling(BaseModel):
    verdict_summary: str = Field(description="A short, authoritative summary of the decision.")
    send_back_to_defense: bool = Field(description="True if the solution has errors. False if it is perfect.")

def issue_verdict(state: CaseFile):
    """The Final Decision"""
    print("JUDGE: Deciding...")
    
    solution = state.get("proposed_solution", "No solution provided.")
    critique = state.get("prosecutor_critique", "No critique provided.")
    
    structured_llm = llm.with_structured_output(JudicialRuling)
    
    prompt = f"""
    You are the High Court Judge.
    
    Defense Submission:
    {solution}
    
    Prosecution Argument:
    {critique}
    
    Review the arguments. If the Prosecution found valid fatal errors, rule to send it back.
    If the Prosecution is merely nitpicking, rule in favor of the Defense.
    """
    
    ruling = structured_llm.invoke(prompt)
    
    return {
        "verdict": ruling.verdict_summary,
        "is_guilty": ruling.send_back_to_defense
    }