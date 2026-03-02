import os
from langchain_openai import ChatOpenAI

def get_gemini_client(model_name: str = "gemini-3-flash", temperature: float = 0.0, **kwargs) -> ChatOpenAI:
    """
    Returns a LangChain ChatOpenAI client configured to use the local Gemini API proxy.
    
    Args:
        model_name: The name of the model to use (default: gemini-3-flash).
        temperature: The sampling temperature.
        **kwargs: Additional arguments to pass to the ChatOpenAI constructor.
        
    Returns:
        A configured ChatOpenAI instance.
    """
    # Use local proxy as the default base URL
    base_url = os.getenv("GEMINI_API_BASE", "http://localhost:8888/v1/")
    
    # The proxy might require an API key (GEMINI_AUTH_PASSWORD in its config)
    api_key = os.getenv("GEMINI_API_KEY", "dummy-key")
    
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        openai_api_base=base_url,
        api_key=api_key,
        **kwargs
    )
