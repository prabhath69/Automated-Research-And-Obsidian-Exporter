from typing import TypedDict, List, Dict, Optional
from app.models.schemas import ResearchPlan, ResearchTask, Source, SourceEvaluation, Evidence, Claim, Critique, ObsidianNote

class ResearchState(TypedDict):
    research_id: str
    original_query: str
    
    # Planning
    research_plan: Optional[ResearchPlan]
    research_tasks: List[ResearchTask]
    
    # Research & Extraction
    collected_sources: List[Source]
    source_evaluations: Dict[str, SourceEvaluation]  # Mapping source_id to its evaluation
    evidence: List[Evidence]
    
    # Synthesis
    claims: List[Claim]
    draft_report: str
    
    # Critique & Refinement
    critique: Optional[Critique]
    iteration_count: int
    
    # Final Output
    final_report: str
    obsidian_notes: List[ObsidianNote]
    errors: List[str]
