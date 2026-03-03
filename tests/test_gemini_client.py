import pytest
from gemini_driven_img2md.gemini_client import get_gemini_client
from langchain_google_genai import ChatGoogleGenerativeAI

def test_get_gemini_client():
    """Test that the client is initialized correctly as ChatGoogleGenerativeAI."""
    client = get_gemini_client()
    assert isinstance(client, ChatGoogleGenerativeAI)
    assert "gemini-3-flash" in client.model
    assert client.transport == "rest"

def test_client_initialization_with_custom_params():
    """Verify that the client can be initialized with custom settings."""
    client = get_gemini_client(temperature=0.1)
    assert client.temperature == 0.1
