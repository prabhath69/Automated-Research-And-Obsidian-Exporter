from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from app.services.llm import get_structured_llm
from app.models.schemas import Claim, Evidence
from app.models.state import ResearchState
import uuid
import logging

logger = logging.getLogger(__name__)

class ClaimList(BaseModel):
    items: List[Claim] = Field(description="List of synthesized claims based on evidence")

CLAIM_PROMPT = """
You are a senior analyst. 
Review the following extracted evidence items and synthesize them into high-level, factual claims.
Each claim must explicitly list the evidence IDs that support it.
Do NOT invent claims. Every claim must be strictly supported by the provided evidence.
You can combine multiple evidence items into a single claim if they agree or complement each other.

Evidence Items:
{evidence_text}
"""

def generate_claims(state: ResearchState) -> dict:
    """LangGraph node to generate claims from extracted evidence."""
    evidence_list = state.get("evidence", [])
    existing_claims = state.get("claims", [])
    
    # Simple check: if we haven't extracted new evidence, we might not need to regenerate everything,
    # but for simplicity, we'll re-synthesize claims from all evidence in each iteration.
    if not evidence_list:
        return {}
        
    logger.info(f"Generating claims from {len(evidence_list)} evidence items.")
    
    evidence_text = ""
    for e in evidence_list:
        evidence_text += f"[ID: {e.evidence_id} | Source: {e.source_id}]\nContent: {e.relevant_passage}\n\n"
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", CLAIM_PROMPT),
        ("user", "Synthesize claims now.")
    ])
    
    llm = get_structured_llm(ClaimList)
    chain = prompt | llm
    
    try:
        result = chain.invoke({
            "evidence_text": evidence_text
        })
        
        new_claims = []
        for claim in result.items:
            claim.claim_id = f"C-{str(uuid.uuid4())[:6]}"
            new_claims.append(claim)
            
        # For simplicity, we overwrite claims each iteration based on cumulative evidence
        return {"claims": new_claims}
        
    except Exception as e:
        logger.error(f"Error generating claims: {e}")
        return {"claims": existing_claims}
