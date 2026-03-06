import pytest
from src.gemini_driven_img2md.mcp_server import mcp

@pytest.mark.asyncio
async def test_mcp_tool_registration():
    """Verify that tools are correctly registered in the FastMCP instance."""
    tools = await mcp.list_tools()
    tool_names = [t.name for t in tools]
    
    assert "profile_document" in tool_names
    assert "extract_page" in tool_names

@pytest.mark.asyncio
async def test_mcp_tool_definitions():
    """Check if tool arguments are correctly defined."""
    tools = await mcp.list_tools()
    
    extract_tool = next(t for t in tools if t.name == "extract_page")
    # FastMCP uses Pydantic/inspect to get schema
    assert "pdf_path" in extract_tool.inputSchema["properties"]
    assert "page" in extract_tool.inputSchema["properties"]
