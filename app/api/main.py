from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.graph.workflow import create_research_graph
from app.models.state import ResearchState
import uuid
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s:     %(name)s - %(message)s')

app = FastAPI(title="Automated Research Synthesizer API")

# Initialize graph
research_graph = create_research_graph()

import sqlite3
import json

from fastapi.encoders import jsonable_encoder

def get_db():
    conn = sqlite3.connect("research_jobs.db", check_same_thread=False)
    conn.execute("CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, data TEXT)")
    return conn

def save_job(research_id: str, data: dict):
    conn = get_db()
    with conn:
        # Use jsonable_encoder to handle Pydantic models in the state
        serializable_data = jsonable_encoder(data)
        conn.execute("INSERT OR REPLACE INTO jobs (id, data) VALUES (?, ?)", (research_id, json.dumps(serializable_data)))

def load_job(research_id: str) -> dict:
    conn = get_db()
    cur = conn.execute("SELECT data FROM jobs WHERE id = ?", (research_id,))
    row = cur.fetchone()
    if row:
        return json.loads(row[0])
    return None

class ResearchRequest(BaseModel):
    query: str

class ResearchResponse(BaseModel):
    research_id: str
    status: str

@app.post("/research", response_model=ResearchResponse)
async def start_research(request: ResearchRequest):
    research_id = str(uuid.uuid4())
    
    # Initialize state
    initial_state: ResearchState = {
        "research_id": research_id,
        "original_query": request.query,
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
    
    # Run asynchronously (for this MVP, we run synchronously in background using invoke,
    # but FastAPI allows async. For simplicity, we just invoke it here. 
    # In a real app, this should be a background task.)
    
    try:
        # We'll run it synchronously for the MVP to easily fetch results.
        # Alternatively, we can use BackgroundTasks.
        final_state = research_graph.invoke(initial_state)
        save_job(research_id, final_state)
        return {"research_id": research_id, "status": "completed"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        save_job(research_id, {"errors": [str(e)]})
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/research/{research_id}")
async def get_research(research_id: str):
    job = load_job(research_id)
    if not job:
        raise HTTPException(status_code=404, detail="Research not found")
    return job
