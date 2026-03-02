from gemini_driven_img2md.prompts import get_extraction_prompt

def test_get_extraction_prompt():
    """Verify that the extraction prompt contains key instructions."""
    prompt = get_extraction_prompt()
    assert "Markdown" in prompt
    assert "LaTeX" in prompt
    assert "literal caption" in prompt
    assert "json" in prompt.lower()
