from langchain_core.prompts import ChatPromptTemplate
from app.services.llm import get_structured_llm
from app.models.schemas import Critique
from app.models.state import ResearchState
import logging

logger = logging.getLogger(__name__)

CRITIC_PROMPT = """
You are a rigorous research critic.
Review the draft research report against the original query and research plan.
Identify any unsupported claims, missing topics, or conflicting evidence.
If there are significant gaps, generate specific recommended research tasks to fill them.
Determine if the report is sufficient to be finalized (is_sufficient = true/false).
If iteration_count >= max_iterations, you must set is_sufficient = true to prevent infinite loops.

Original Query: {query}
Iteration Count: {iteration_count}
Max Iterations: {max_iterations}

Draft Report:
{draft_report}
"""

def critique_report(state: ResearchState) -> dict:
    """LangGraph node to critique the draft report."""
    query = state.get("original_query", "")
    draft = state.get("draft_report", "")
    iteration_count = state.get("iteration_count", 0)
    from app.config.settings import settings
    
    logger.info(f"Critiquing report (Iteration {iteration_count}).")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", CRITIC_PROMPT),
        ("user", "Critique the report.")
    ])
    
    llm = get_structured_llm(Critique)
    chain = prompt | llm
    
    try:
        critique_result = chain.invoke({
            "query": query,
            "iteration_count": iteration_count,
            "max_iterations": settings.MAX_ITERATIONS,
            "draft_report": draft
        })
        
        # Safety override
        if iteration_count >= settings.MAX_ITERATIONS:
            critique_result.is_sufficient = True
            
        return {
            "critique": critique_result,
            "iteration_count": iteration_count + 1
        }
    except Exception as e:
        logger.error(f"Error critiquing report: {e}")
        # Fallback to finish
        fallback = Critique(
            unsupported_claims=[],
            missing_topics=[],
            conflicting_evidence=[],
            recommended_research_tasks=[],
            overall_score=50,
            is_sufficient=True
        )
        return {
            "critique": fallback,
            "iteration_count": iteration_count + 1
        }
