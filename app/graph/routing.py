from typing import Literal
from app.models.state import ResearchState
import logging

logger = logging.getLogger(__name__)

def route_after_critique(state: ResearchState) -> Literal["researcher", "obsidian_exporter"]:
    """Conditional edge router after critique."""
    critique = state.get("critique")
    
    if critique and not critique.is_sufficient:
        logger.info("Report is insufficient. Routing back to researcher.")
        # If the critic recommended new tasks, we add them to the state's research_tasks.
        # This modification of state should ideally happen in a node, 
        # so let's assume a small 'refinement_node' adds them before routing,
        # or we just route to a 'refinement' node which then goes to 'researcher'.
        # For simplicity, we can just route to a refinement node.
        return "refinement_node"
    
    logger.info("Report is sufficient. Routing to exporter.")
    return "obsidian_exporter"

def refinement_node(state: ResearchState) -> dict:
    """Adds critic's recommended tasks to the pending task list."""
    critique = state.get("critique")
    tasks = state.get("research_tasks", [])
    
    if critique and critique.recommended_research_tasks:
        for t in critique.recommended_research_tasks:
            t.status = "pending"
            tasks.append(t)
            
    return {"research_tasks": tasks}
