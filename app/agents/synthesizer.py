from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.services.llm import get_llm
from app.models.state import ResearchState
import logging

logger = logging.getLogger(__name__)

SYNTHESIZER_PROMPT = """
You are an expert technical writer.
Draft a comprehensive research report based on the provided claims and original research query.
You must cite the source IDs provided in the claims using the format [SourceID].
Do NOT include any claims or facts that are not provided in the claims list.
Ensure the report flows logically and is well-structured in Markdown.

Research Query:
{query}

Claims and Sources:
{claims_text}

Format the report with clear headings, subheadings, and bullet points where appropriate.
Include a "Sources" section at the end if you want, but inline citations are mandatory.
"""

def synthesize_report(state: ResearchState) -> dict:
    """LangGraph node to synthesize a draft report from claims."""
    query = state.get("original_query", "")
    claims = state.get("claims", [])
    
    if not claims:
        return {"draft_report": "No claims could be generated from the gathered evidence."}
        
    logger.info(f"Synthesizing report from {len(claims)} claims.")
    
    claims_text = ""
    for c in claims:
        claims_text += f"- {c.statement} (Sources: {', '.join(c.source_ids)})\n"
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYNTHESIZER_PROMPT),
        ("user", "Write the report.")
    ])
    
    llm = get_llm()
    chain = prompt | llm | StrOutputParser()
    
    try:
        report = chain.invoke({
            "query": query,
            "claims_text": claims_text
        })
        return {"draft_report": report}
    except Exception as e:
        logger.error(f"Error synthesizing report: {e}")
        return {"draft_report": f"Error generating report: {e}"}
