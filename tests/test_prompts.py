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
    assert "visual_matchers" in prompt
    assert "layout_info" in prompt

def test_get_extraction_prompt_triplet():
    """Verify that extraction prompt mentions triplet context."""
    from gemini_driven_img2md.prompts import get_extraction_prompt
    prompt = get_extraction_prompt(style_profile='{"rules": "test"}')
    assert "GLOBAL STYLE REGISTRY" in prompt
    assert "TARGET PAGE" in prompt
    assert "PREVIOUS PAGE" in prompt
    assert "NEXT PAGE" in prompt
    assert "Target-Only Extraction" in prompt
    assert "style_conformity" in prompt
    assert "style_patch" in prompt
