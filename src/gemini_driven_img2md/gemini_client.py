import os
from langchain_google_genai import ChatGoogleGenerativeAI
from google.generativeai import configure

def get_gemini_client(model_name: str = "gemini-3-flash", temperature: float = 0.0, **kwargs) -> ChatGoogleGenerativeAI:
    """
    Returns a LangChain ChatGoogleGenerativeAI client configured to use the native Gemini API proxy.
    
    Args:
        model_name: The name of the model to use (default: gemini-3-flash).
        temperature: The sampling temperature.
        **kwargs: Additional arguments to pass to the ChatGoogleGenerativeAI constructor.
        
    Returns:
        A configured ChatGoogleGenerativeAI instance.
    """
    # Get configuration from environment
    api_key = os.getenv("GEMINI_API_KEY", "dummy-key")
    # Native endpoint usually points to the host:port
    api_endpoint = os.getenv("GEMINI_API_ENDPOINT", "http://localhost:8888")
    
    # Configure the underlying google-generativeai SDK to point to the proxy
    # The client_options 'api_endpoint' is the standard way to redirect the SDK.
    # Note: We must strip the http:// for the api_endpoint in some SDK versions, 
    # but geminicli2api-async expects the full authority or proxied path.
    
    # Remove http:// for the SDK endpoint configuration if necessary
    sdk_endpoint = api_endpoint.replace("http://", "").replace("https://", "")
    
    configure(
        api_key=api_key,
        client_options={"api_endpoint": sdk_endpoint}
    )
    
    # Return the LangChain wrapper
    # transport="rest" is often required for proxies
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        google_api_key=api_key,
        transport="rest",
        **kwargs
    )
