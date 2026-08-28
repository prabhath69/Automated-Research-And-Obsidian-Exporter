from langgraph.graph import StateGraph, END
from app.models.state import ResearchState
from app.agents.planner import plan_research
from app.agents.task_generator import generate_tasks
from app.agents.researcher import conduct_research
from app.agents.evaluator import evaluate_sources
from app.agents.extractor import extract_evidence
from app.agents.claim_generator import generate_claims
from app.agents.synthesizer import synthesize_report
from app.agents.critic import critique_report
from app.graph.routing import route_after_critique, refinement_node
from app.exporters.obsidian import generate_obsidian_notes

def create_research_graph():
    """Builds and compiles the LangGraph research workflow."""
    workflow = StateGraph(ResearchState)
    
    # Add Nodes
    workflow.add_node("planner", plan_research)
    workflow.add_node("task_generator", generate_tasks)
    workflow.add_node("researcher", conduct_research)
    workflow.add_node("evaluator", evaluate_sources)
    workflow.add_node("extractor", extract_evidence)
    workflow.add_node("claim_generator", generate_claims)
    workflow.add_node("synthesizer", synthesize_report)
    workflow.add_node("critic", critique_report)
    workflow.add_node("refinement_node", refinement_node)
    workflow.add_node("obsidian_exporter", generate_obsidian_notes)
    
    # Define Edges
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "task_generator")
    workflow.add_edge("task_generator", "researcher")
    workflow.add_edge("researcher", "evaluator")
    workflow.add_edge("evaluator", "extractor")
    workflow.add_edge("extractor", "claim_generator")
    workflow.add_edge("claim_generator", "synthesizer")
    workflow.add_edge("synthesizer", "critic")
    
    # Conditional Routing
    workflow.add_conditional_edges(
        "critic",
        route_after_critique,
        {
            "refinement_node": "refinement_node",
            "obsidian_exporter": "obsidian_exporter"
        }
    )
    
    # Loop back
    workflow.add_edge("refinement_node", "researcher")
    
    # End
    workflow.add_edge("obsidian_exporter", END)
    
    return workflow.compile()
