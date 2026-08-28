from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional

class ResearchTask(BaseModel):
    task_id: str = Field(description="Unique identifier for this task")
    question: str = Field(description="The specific sub-question to research")
    objective: str = Field(description="What information we are trying to find")
    search_queries: List[str] = Field(description="Specific search queries to execute")
    status: str = Field(default="pending", description="Status of the task (pending, completed, failed)")

class ResearchPlan(BaseModel):
    main_objective: str = Field(description="The overall research goal")
    sub_questions: List[str] = Field(description="Decomposed sub-questions")

class Source(BaseModel):
    source_id: str = Field(description="Unique identifier for the source (e.g., S1, S2)")
    url: str = Field(description="URL of the source")
    title: str = Field(description="Title of the page")
    publisher: Optional[str] = Field(None, description="Publisher or domain")
    content: str = Field(description="Extracted content or snippet")
    task_id: str = Field(description="The ID of the task this source was found for")

class SourceEvaluation(BaseModel):
    source_id: str = Field(description="The ID of the source being evaluated")
    relevance_score: int = Field(description="Score 1-10 for relevance to the task")
    authority_score: int = Field(description="Score 1-10 for authority/credibility")
    overall_score: int = Field(description="Average or weighted total score")
    keep: bool = Field(description="Whether to keep this source for evidence extraction")
    reason: str = Field(description="Reasoning for keeping or discarding")

class Evidence(BaseModel):
    evidence_id: str = Field(description="Unique identifier (e.g., E1, E2)")
    source_id: str = Field(description="Source this evidence came from")
    task_id: str = Field(description="The task this evidence addresses")
    relevant_passage: str = Field(description="The specific fact, quote, or data extracted")
    confidence: int = Field(description="Confidence score 1-10")

class Claim(BaseModel):
    claim_id: str = Field(description="Unique identifier (e.g., C1, C2)")
    statement: str = Field(description="The synthesized factual claim")
    evidence_ids: List[str] = Field(description="List of evidence IDs supporting this claim")
    source_ids: List[str] = Field(description="List of source IDs supporting this claim")

class Critique(BaseModel):
    unsupported_claims: List[str] = Field(description="Claims lacking sufficient evidence")
    missing_topics: List[str] = Field(description="Topics from the plan that were not addressed")
    conflicting_evidence: List[str] = Field(description="Any contradictions found")
    recommended_research_tasks: List[ResearchTask] = Field(description="New tasks to resolve gaps")
    overall_score: int = Field(description="Quality score 1-100")
    is_sufficient: bool = Field(description="True if the report is good enough to finalize")

class ObsidianNote(BaseModel):
    title: str = Field(description="Note title without extension")
    content: str = Field(description="Markdown content including frontmatter")
