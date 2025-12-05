from app.court.state import CaseFile
from app.services.llm import get_llm
from app.core.config import settings
from langchain_core.messages import HumanMessage

# Uses Llama 4 Scout (The Vision Expert)
llm = get_llm(settings.MODEL_EVIDENCE_ANALYZER, temperature=0.2)

def analyze_evidence(state: CaseFile):
    """The Investigator (Vision Analysis)"""
    print("INVESTIGATOR: Analyzing visual evidence...")
    
    image_url = state.get("image_url")
    query = state["original_query"]
    
    if not image_url:
        return {"prosecutor_critique": "No visual evidence provided."}

    # Accepts images directly in the message payload
    message = HumanMessage(
        content=[
            {"type": "text", "text": f"Analyze this UI/Diagram for the following request: {query}"},
            {
                "type": "image_url",
                "image_url": {"url": image_url}
            }
        ]
    )
    
    # Identifies visual bugs, layout issues, or extracts text from diagrams
    response = llm.invoke([message])
    
    return {
        # Append the visual findings to the prompt context for the other agents
        "original_query": f"{query}\n\n[VISUAL EVIDENCE ANALYSIS]: {response.content}"
    }