from gemini_driven_img2md.prompts import get_extraction_prompt, get_profiler_prompt

def test_get_extraction_prompt_sota():
    """Verify that the SOTA extraction prompt contains critical logic."""
    prompt = get_extraction_prompt()
    # Basic requirements
    assert "Markdown" in prompt
    assert "LaTeX" in prompt
    assert "caption" in prompt.lower()
    
    # SOTA additions
    assert "bbox" in prompt.lower()
    assert "[ymin, xmin, ymax, xmax]" in prompt
    assert "normalized" in prompt.lower()
    assert "TARGET PAGE" in prompt.upper()

def test_get_profiler_prompt():
    """Verify the Stage 0 profiler prompt structure."""
    prompt = get_profiler_prompt()
    assert "Style Registry" in prompt
    assert "heading_weights" in prompt
    assert "visual_matchers" in prompt
    assert "json" in prompt.lower()

def test_get_extraction_prompt_triplet():
    """Verify that extraction prompt mentions triplet context."""
    prompt = get_extraction_prompt(style_profile='{"rules": "test"}')
    assert "STYLE REGISTRY" in prompt.upper()
    assert "TARGET PAGE" in prompt.upper()
    assert "PREVIOUS PAGE" in prompt.upper()
    assert "NEXT PAGE" in prompt.upper()
