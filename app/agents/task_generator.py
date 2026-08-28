from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from app.services.llm import get_structured_llm
from app.models.schemas import ResearchTask
from app.models.state import ResearchState
import uuid

class TaskList(BaseModel):
    tasks: List[ResearchTask] = Field(description="List of research tasks to execute")

TASK_GEN_PROMPT = """
You are a senior AI research assistant. 
Based on the following research plan and sub-questions, generate specific, actionable research tasks.
Each task must include a specific objective and a list of search queries.
Generate exactly one task per sub-question.

Main Objective:
{main_objective}

Sub-Questions:
{sub_questions}
"""

def generate_tasks(state: ResearchState) -> dict:
    """LangGraph node to generate research tasks from the plan."""
    plan = state["research_plan"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", TASK_GEN_PROMPT),
        ("user", "Main Objective: {main_objective}\nSub-Questions:\n{sub_questions}")
    ])
    
    llm = get_structured_llm(TaskList)
    chain = prompt | llm
    
    result = chain.invoke({
        "main_objective": plan.main_objective,
        "sub_questions": "\n".join(f"- {q}" for q in plan.sub_questions)
    })
    
    # Ensure task IDs are unique and structured
    for i, task in enumerate(result.tasks):
        task.task_id = f"T{i+1}-{str(uuid.uuid4())[:4]}"
        task.status = "pending"
        
    return {"research_tasks": result.tasks}
