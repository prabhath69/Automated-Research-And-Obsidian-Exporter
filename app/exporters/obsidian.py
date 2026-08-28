from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from app.services.llm import get_structured_llm
from app.models.schemas import ObsidianNote
from app.models.state import ResearchState
import os
import datetime
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class NoteCollection(BaseModel):
    notes: List[ObsidianNote] = Field(description="A collection of interconnected Markdown notes")

OBSIDIAN_PROMPT = """
You are an expert knowledge manager.
Convert the following research report into a set of interconnected Obsidian notes.
Do not just output one file. Create a main "Overview" note and several specific sub-topic notes.
Use wikilinks like [[Note Title]] to link them together where semantically useful.
Each note must have YAML frontmatter with title, tags, and a dynamically generated date.

Current Date: {date}

Report to convert:
{report}
"""

def generate_obsidian_notes(state: ResearchState) -> dict:
    """LangGraph node to convert the report into Obsidian notes."""
    report = state.get("draft_report", "")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", OBSIDIAN_PROMPT),
        ("user", "Convert this report to Obsidian notes.")
    ])
    
    llm = get_structured_llm(NoteCollection)
    chain = prompt | llm
    
    try:
        result = chain.invoke({
            "date": datetime.date.today().isoformat(),
            "report": report
        })
        
        # Save files to disk
        vault_path = settings.OBSIDIAN_VAULT_PATH
        os.makedirs(vault_path, exist_ok=True)
        
        for note in result.notes:
            safe_title = "".join(c for c in note.title if c.isalnum() or c in " _-").rstrip()
            file_path = os.path.join(vault_path, f"{safe_title}.md")
            
            # Simple collision detection / overwrite
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(note.content)
                
            logger.info(f"Exported Obsidian note: {file_path}")
            
        return {
            "obsidian_notes": result.notes,
            "final_report": report # The draft becomes final here
        }
    except Exception as e:
        logger.error(f"Error generating Obsidian notes: {e}")
        return {"errors": [f"Obsidian export failed: {e}"]}
