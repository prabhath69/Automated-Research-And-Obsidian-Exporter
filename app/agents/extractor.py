from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from app.services.llm import get_structured_llm
from app.models.schemas import Evidence
from app.models.state import ResearchState
import uuid
import logging

logger = logging.getLogger(__name__)

class EvidenceList(BaseModel):
    items: List[Evidence] = Field(description="List of evidence items extracted")

EXTRACTOR_PROMPT = """
You are a meticulous research evidence extractor.
Analyze the provided source content and extract specific, factual claims or data points relevant to the research task.
Do NOT hallucinate. Only extract what is explicitly stated.

Research Task: {task_objective}
Source Title: {source_title}

Content:
{source_content}
"""

def extract_evidence(state: ResearchState) -> dict:
    """LangGraph node to extract specific evidence from retained sources."""
    sources = state.get("collected_sources", [])
    evaluations = state.get("source_evaluations", {})
    existing_evidence = state.get("evidence", [])
    tasks = {t.task_id: t for t in state.get("research_tasks", [])}
    
    # We only process sources we haven't extracted from yet.
    # Keep track of processed sources by looking at existing evidence.
    processed_source_ids = {e.source_id for e in existing_evidence}
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", EXTRACTOR_PROMPT),
        ("user", "Extract evidence now.")
    ])
    
    llm = get_structured_llm(EvidenceList)
    chain = prompt | llm
    
    new_evidence = []
    
    for source in sources:
        if source.source_id in processed_source_ids:
            continue
            
        evaluation = evaluations.get(source.source_id)
        if not evaluation or not evaluation.keep:
            continue
            
        task = tasks.get(source.task_id)
        if not task:
            continue
            
        logger.info(f"Extracting evidence from source: {source.source_id}")
        
        try:
            result = chain.invoke({
                "task_objective": task.objective,
                "source_title": source.title,
                "source_content": source.content[:4000] # Limiting context window
            })
            
            for item in result.items:
                item.evidence_id = f"E-{str(uuid.uuid4())[:6]}"
                item.source_id = source.source_id
                item.task_id = source.task_id
                new_evidence.append(item)
                
        except Exception as e:
            logger.error(f"Error extracting evidence from {source.source_id}: {e}")
            
    return {"evidence": existing_evidence + new_evidence}
