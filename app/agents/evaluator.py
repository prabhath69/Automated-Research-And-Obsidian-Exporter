from langchain_core.prompts import ChatPromptTemplate
from app.services.llm import get_structured_llm
from app.models.schemas import SourceEvaluation
from app.models.state import ResearchState
import logging

logger = logging.getLogger(__name__)

EVALUATOR_PROMPT = """
You are a research source evaluator.
Evaluate the following source for its relevance to the given research task and its general authority/credibility.

Research Task: {task_objective}
Source Title: {source_title}
Source URL: {source_url}

Snippet/Content:
{source_content}

Provide a structured evaluation including scores (1-10) and whether to keep or discard this source.
A source should be kept if it provides factual, relevant evidence for the task.
"""

def evaluate_sources(state: ResearchState) -> dict:
    """LangGraph node to evaluate collected sources."""
    sources = state.get("collected_sources", [])
    tasks = {t.task_id: t for t in state.get("research_tasks", [])}
    evaluations = state.get("source_evaluations", {})
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", EVALUATOR_PROMPT),
        ("user", "Evaluate this source.")
    ])
    
    llm = get_structured_llm(SourceEvaluation)
    chain = prompt | llm
    
    new_evaluations = {**evaluations}
    
    for source in sources:
        if source.source_id in new_evaluations:
            continue
            
        task = tasks.get(source.task_id)
        if not task:
            continue
            
        logger.info(f"Evaluating source: {source.url}")
        
        try:
            eval_result = chain.invoke({
                "task_objective": task.objective,
                "source_title": source.title,
                "source_url": source.url,
                "source_content": source.content[:2000] # Pass snippet to save context
            })
            
            # Ensure the source ID matches
            eval_result.source_id = source.source_id
            new_evaluations[source.source_id] = eval_result
        except Exception as e:
            logger.error(f"Error evaluating source {source.source_id}: {e}")
            # Fallback evaluation
            new_evaluations[source.source_id] = SourceEvaluation(
                source_id=source.source_id,
                relevance_score=5,
                authority_score=5,
                overall_score=5,
                keep=False,
                reason=f"Evaluation failed: {e}"
            )
            
    return {"source_evaluations": new_evaluations}
