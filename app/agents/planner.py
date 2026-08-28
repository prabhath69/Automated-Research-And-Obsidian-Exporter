from langchain_core.prompts import ChatPromptTemplate
from app.services.llm import get_structured_llm
from app.models.schemas import ResearchPlan
from app.models.state import ResearchState

PLANNER_PROMPT = """
You are a senior AI research planner.
Your goal is to decompose the user's research query into a structured research plan.
You must break the main objective down into specific, non-overlapping sub-questions.
Do not provide answers, only plan the research process.

User Query:
{query}
"""

def plan_research(state: ResearchState) -> dict:
    """LangGraph node to generate the research plan."""
    query = state["original_query"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", PLANNER_PROMPT),
        ("user", "{query}")
    ])
    
    llm = get_structured_llm(ResearchPlan)
    chain = prompt | llm
    
    plan = chain.invoke({"query": query})
    
    # We return a dict with the fields to update in the state
    return {"research_plan": plan}
