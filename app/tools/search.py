import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

def search_duckduckgo(query: str, max_results: int = 3) -> list[dict]:
    """Search DuckDuckGo and return a list of results."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return [{"title": r["title"], "url": r["href"], "snippet": r["body"]} for r in results]
    except Exception as e:
        logger.error(f"DuckDuckGo search failed for query '{query}': {e}")
        return []

def fetch_page_content(url: str, timeout: int = 10) -> str:
    """Fetch the text content of a webpage."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.extract()
            
        text = soup.get_text(separator=' ', strip=True)
        # Limit content size to avoid context overflow
        return text[:10000] 
    except Exception as e:
        logger.warning(f"Failed to fetch page {url}: {e}. Falling back to snippet.")
        return ""

def execute_search_task(query: str) -> list[dict]:
    """Executes a search and fetches content for the top results."""
    # Use DDG
    results = search_duckduckgo(query, max_results=settings.MAX_SOURCES_PER_TASK)
    
    for result in results:
        # We try to fetch the full page, if it fails, we fall back to the snippet
        content = fetch_page_content(result["url"])
        result["content"] = content if content else result["snippet"]
        
    return results
