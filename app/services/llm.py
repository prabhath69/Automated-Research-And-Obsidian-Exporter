from langchain_openai import AzureChatOpenAI
from app.config.settings import settings

def get_llm():
    """Returns the configured AzureChatOpenAI instance."""
    return AzureChatOpenAI(
        api_key=settings.AZURE_OPENAI_API_KEY,
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT,
        api_version=settings.AZURE_OPENAI_API_VERSION,
        temperature=0.1,  # Low temperature for analytical tasks
    )

def get_structured_llm(schema):
    """Returns an LLM bound to a specific Pydantic schema."""
    llm = get_llm()
    return llm.with_structured_output(schema)
