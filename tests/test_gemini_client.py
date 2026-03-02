import pytest
from gemini_driven_img2md.gemini_client import get_gemini_client
from langchain_openai import ChatOpenAI

def test_get_gemini_client():
    """Test that the client is initialized correctly using the local proxy."""
    client = get_gemini_client()
    assert isinstance(client, ChatOpenAI)
    assert client.model_name == "gemini-3-flash"
    assert str(client.openai_api_base) == "http://localhost:8888/v1/"

def test_client_initialization_with_custom_params():
    """Verify that the client can be initialized with custom settings."""
    client = get_gemini_client(temperature=0.1)
    assert client.temperature == 0.1
