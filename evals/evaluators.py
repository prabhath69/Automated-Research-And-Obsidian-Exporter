from langsmith.schemas import Run, Example
from app.services.llm import get_structured_llm
from pydantic import BaseModel, Field

class RelevanceScore(BaseModel):
    score: int = Field(description="Score from 1 to 5 indicating how relevant the report is to the query.")
    reason: str = Field(description="Reasoning for the score.")

def relevance_evaluator(run: Run, example: Example) -> dict:
    """Evaluates if the generated report answers the user's initial query."""
    query = example.inputs["query"]
    final_report = run.outputs.get("final_report", "")
    errors = run.outputs.get("errors", [])
    
    if "expected_errors" in example.outputs:
        expected_error_substr = example.outputs["expected_errors"][0]
        if any(expected_error_substr in e for e in errors):
            return {"key": "guardrail_success", "score": 1}
        else:
            return {"key": "guardrail_success", "score": 0}
            
    if not final_report:
        return {"key": "relevance", "score": 0, "comment": "No report generated"}
        
    llm = get_structured_llm(RelevanceScore)
    prompt = f"""
    Evaluate the relevance of the following research report to the user query.
    Score from 1 (completely irrelevant) to 5 (perfectly answers the query).
    
    User Query: {query}
    
    Report preview (first 2000 chars):
    {final_report[:2000]}
    """
    
    result = llm.invoke(prompt)
    
    # Normalize score between 0 and 1
    normalized_score = (result.score - 1) / 4.0
    
    return {
        "key": "relevance",
        "score": normalized_score,
        "comment": result.reason
    }

class FaithfulnessScore(BaseModel):
    is_faithful: bool = Field(description="True if all claims in the report are supported by the provided evidence.")
    reason: str = Field(description="Reasoning for the decision.")

def faithfulness_evaluator(run: Run, example: Example) -> dict:
    """Evaluates if the final report hallucinates beyond the extracted evidence."""
    final_report = run.outputs.get("final_report", "")
    claims = run.outputs.get("claims", [])
    
    if not final_report or not claims:
        return {"key": "faithfulness", "score": 1} # N/A if failed earlier, don't penalize faithfulness
        
    evidence_text = "\n".join([f"- {c.statement} (Source: {c.source_id})" for c in claims])
    
    llm = get_structured_llm(FaithfulnessScore)
    prompt = f"""
    Evaluate the faithfulness of the following research report against the provided evidence.
    Are all the claims made in the report directly supported by the evidence?
    
    Evidence:
    {evidence_text}
    
    Report preview:
    {final_report[:2000]}
    """
    
    result = llm.invoke(prompt)
    
    return {
        "key": "faithfulness",
        "score": 1 if result.is_faithful else 0,
        "comment": result.reason
    }
