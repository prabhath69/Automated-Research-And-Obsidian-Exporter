from app.models.state import ResearchState
from app.models.schemas import Source
from app.tools.search import execute_search_task
from app.config.settings import settings
import uuid
import logging

logger = logging.getLogger(__name__)

def conduct_research(state: ResearchState) -> dict:
    """LangGraph node to execute search tasks and collect sources."""
    tasks = state.get("research_tasks", [])
    collected_sources = state.get("collected_sources", [])
    
    new_sources = []
    
    # We only process pending tasks
    for task in tasks:
        if task.status != "pending":
            continue
            
        logger.info(f"Executing research task: {task.task_id} - {task.question}")
        
        # Take the first query for simplicity, or iterate
        if not task.search_queries:
            task.status = "failed"
            continue
            
        query = task.search_queries[0]
        results = execute_search_task(query)
        
        for i, res in enumerate(results):
            source = Source(
                source_id=f"S-{task.task_id}-{i}-{str(uuid.uuid4())[:4]}",
                url=res["url"],
                title=res["title"],
                content=res["content"],
                task_id=task.task_id
            )
            new_sources.append(source)
            
        task.status = "completed"
        
    return {
        "collected_sources": collected_sources + new_sources,
        "research_tasks": tasks  # Return updated tasks (status changed)
    }
