from typing import TypedDict, List, Optional, Annotated
import operator
from langchain_core.messages import BaseMessage

class CaseFile(TypedDict):
    """
    The CaseFile represents the shared state of the court session.
    It acts as the folder of evidence passed from agent to agent.
    """
    # INPUTS
    original_query: str                  # The user's text prompt
    image_url: Optional[str]             # (Optional) Screenshot/Diagram URL

    # AUXILIARY DATA
    relevant_context: Optional[str]      # Past precedents recalled by Archivist
    
    # AGENT OUTPUTS
    visual_analysis: Optional[str]       # What the Investigator saw (Llama 4 Scout)
    proposed_solution: str               # The Code/Essay written by Defense (GPT-OSS-20B)
    prosecutor_critique: str             # The Flaws found by Prosecutor (Llama 3.3)
    verdict: str                         # The Final Ruling by Judge (GPT-OSS-120B)
    
    # CONTROL FLOW
    is_guilty: bool                      # True = Needs Retry, False = Case Closed
    revision_count: int                  # Safety counter to prevent infinite loops
    
    # HISTORY (Required by LangGraph for memory)
    messages: Annotated[List[BaseMessage], operator.add]