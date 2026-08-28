import os
import traceback
from app.graph.workflow import create_research_graph

def main():
    try:
        graph = create_research_graph()
        initial_state = {
            "research_id": "123",
            "original_query": "How are AI agents being used in supply-chain logistics?",
            "research_plan": None,
            "research_tasks": [],
            "collected_sources": [],
            "source_evaluations": {},
            "evidence": [],
            "claims": [],
            "draft_report": "",
            "critique": None,
            "iteration_count": 0,
            "final_report": "",
            "obsidian_notes": [],
            "errors": []
        }
        graph.invoke(initial_state)
        print("Success")
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    main()
