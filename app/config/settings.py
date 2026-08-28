from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_DEPLOYMENT: str
    AZURE_OPENAI_API_VERSION: str
    
    OBSIDIAN_VAULT_PATH: str = "./output"
    
    TAVILY_API_KEY: Optional[str] = None
    USE_TAVILY: bool = False
    
    # Cost control / limits
    MAX_RESEARCH_TASKS: int = 5
    MAX_SOURCES_PER_TASK: int = 3
    MAX_ITERATIONS: int = 3

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
