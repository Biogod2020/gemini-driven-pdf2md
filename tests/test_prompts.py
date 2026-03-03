from gemini_driven_img2md.prompts import get_extraction_prompt

def test_get_extraction_prompt_sota():
    """Verify that the SOTA extraction prompt contains critical logic."""
    prompt = get_extraction_prompt()
    # Basic requirements
    assert "Markdown" in prompt
    assert "LaTeX" in prompt
    assert "literal caption" in prompt
    
    # SOTA additions
    assert "bbox" in prompt.lower()
    assert "[ymin, xmin, ymax, xmax]" in prompt
    assert "normalized coordinates" in prompt
    assert "multi-column" in prompt
    assert "metadata" in prompt

def test_get_profiler_prompt():
    """Verify the Stage 0 profiler prompt structure."""
    from gemini_driven_img2md.prompts import get_profiler_prompt
    prompt = get_profiler_prompt()
    assert "Style Registry" in prompt
    assert "Heading Weights" in prompt
    assert "Visual Matcher" in prompt
    assert "json" in prompt.lower()
