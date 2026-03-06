import os
from langchain_google_genai import ChatGoogleGenerativeAI

def get_gemini_client(model_name: str = "gemini-3-flash-preview", temperature: float = 0.0, **kwargs) -> ChatGoogleGenerativeAI:
    """
    Returns a LangChain ChatGoogleGenerativeAI client configured to use the native Gemini API proxy.
    """
    # The proxy might require an API key (GEMINI_AUTH_PASSWORD in its config)
    api_key = os.getenv("GEMINI_API_KEY", "123456")
    
    # Use the full HTTP URL for the proxy
    api_endpoint = os.getenv("GEMINI_API_ENDPOINT", "http://localhost:8888")
    
    # Pass client_options with the full HTTP endpoint to ChatGoogleGenerativeAI
    # transport="rest" ensures it uses standard HTTP requests
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        google_api_key=api_key,
        transport="rest",
        client_options={
            "api_endpoint": api_endpoint
        },
        **kwargs
    )
