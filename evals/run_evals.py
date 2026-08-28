import os
import sys
# Add the project root to the python path so it can find the 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
from dotenv import load_dotenv
from langsmith import evaluate
from app.graph.workflow import create_research_graph
from evals.dataset import DATASET_NAME
from evals.evaluators import relevance_evaluator, faithfulness_evaluator

load_dotenv()

# Compile the graph
graph = create_research_graph()

def predict(inputs: dict) -> dict:
    """Wrapper to run the LangGraph workflow given an input query."""
    query = inputs["query"]
    
    # Initialize the state
    initial_state = {
        "original_query": query,
        "research_tasks": [],
        "sources": [],
        "claims": [],
        "final_report": "",
        "obsidian_notes": [],
        "errors": [],
        "critique": None,
        "iterations": 0
    }
    
    # Run the graph
    # We use a unique thread_id if we want memory, but for evals we just invoke
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    try:
        final_state = graph.invoke(initial_state, config=config)
        return final_state
    except Exception as e:
        print(f"Graph execution failed: {e}")
        return {"errors": [str(e)]}

def run_evaluations():
    print(f"Starting evaluations for dataset: {DATASET_NAME}")
    
    experiment_results = evaluate(
        predict,
        data=DATASET_NAME,
        evaluators=[relevance_evaluator, faithfulness_evaluator],
        experiment_prefix="Research-Synthesizer-Eval",
        metadata={"version": "1.0", "description": "Baseline evaluation"}
    )
    
    print("\nEvaluation complete! View the results in LangSmith.")

if __name__ == "__main__":
    run_evaluations()
