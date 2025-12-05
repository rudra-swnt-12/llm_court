from langgraph.graph import StateGraph, START, END
from app.court.state import CaseFile
from app.court.roles import proposer, prosecutor, judge, investigator, archivist

def build_court_graph():
    """
    Constructs the StateGraph for the LLM Court.
    Flow: [Investigator?] -> Defense -> Prosecutor -> Judge -> [Loop?]
    """
    workflow = StateGraph(CaseFile)

    # Nodes (The Agents)
    workflow.add_node("archivist", archivist.recall_precedents)
    workflow.add_node("investigator", investigator.analyze_evidence)
    workflow.add_node("defense", proposer.draft_solution)
    workflow.add_node("prosecution", prosecutor.cross_examine)
    workflow.add_node("bench", judge.issue_verdict)

    # Entry Point Logic
    def entry_router(state: CaseFile):
        if state.get("image_url"):
            return "investigator"
        return "defense"

    # Set the Conditional Entry Point
    workflow.add_conditional_edges(
        START,
        entry_router,
        {
            "investigator": "investigator",
            "defense": "defense"
        }
    )

    def memory_router(state: CaseFile):
        if state.get("image_url"):
            return "investigator"
        return "defense"

    workflow.add_conditional_edges(
        "archivist",
        memory_router,
        {"investigator": "investigator", "defense": "defense"}
    )

    # Connecting the Investigator to Defense
    workflow.add_edge("investigator", "defense")

    # Defense (Writes Code) -> Prosecution (Finds Bugs) -> Bench (Decides)
    workflow.add_edge("defense", "prosecution")
    workflow.add_edge("prosecution", "bench")

    # The "Retrial" Logic (The Loop)
    def verdict_router(state: CaseFile):
        if state["revision_count"] >= 3:
            return END
        
        # If Judge says "Guilty" (Bad Code), send back to Defense
        if state["is_guilty"]:
            return "defense"
        
        # Otherwise, Case Closed
        return END

    workflow.add_conditional_edges(
        "bench",
        verdict_router,
        {
            "defense": "defense", # Loop back
            END: END              # Finish
        }
    )
    return workflow.compile()

# Export the compiled graph instance
court_graph = build_court_graph()