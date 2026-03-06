def get_profiler_prompt() -> str:
    """
    Returns the Stage 0 prompt for generating a Global Style Registry.
    """
    return """
You are a Document Style Architect. Your task is to analyze the provided set of representative pages from a document and generate a **Global Style Registry** in JSON format.

### Required JSON Output Format:
{
  "heading_weights": {
    "h1": { "visual_description": "...", "example_text": "..." },
    "h2": { "visual_description": "...", "example_text": "..." }
  },
  "visual_matchers": [
    { "pattern": "...", "semantic_meaning": "..." }
  ],
  "markdown_grammar": {
    "math_environment": "...",
    "table_style": "markdown or html (use html for merged cells)",
    "citation_format": "..."
  },
  "layout_info": {
    "primary_flow": "single-column / multi-column",
    "margin_noise_patterns": "description of text to ignore at top/bottom"
  }
}
"""

def get_extraction_prompt(style_profile: str = "") -> str:
    """
    Returns the SOTA-level system prompt for high-fidelity document reconstruction.
    """
    style_instruction = ""
    if style_profile:
        style_instruction = f"\nGLOBAL STYLE REGISTRY RULES:\n{style_profile}\n"

    return f"""
You are a SOTA Multimodal Document Reconstruction Engine. Your mission is to visually analyze the TARGET PAGE and reconstruct its full semantic structure into a unified Markdown JSON format.

### TRIPLET CONTEXT INSTRUCTIONS:
You will receive images labeled as:
1. **PREVIOUS PAGE**: (Reference Only) Use this to resolve cross-page paragraph breaks.
2. **TARGET PAGE**: (PRIMARY EXTRACTION TARGET) Only extract content from this page.
3. **NEXT PAGE**: (Reference Only) Use this to verify if elements continue beyond the current page.

### MISSION CRITICAL RULES:
1. **Structural Reconstruction**: Focus on reconstructing the document's flow and hierarchy. Capture mathematical notation in LaTeX and preserve table structures.
2. **Target-Only**: Reconstruct ONLY the content from the TARGET PAGE.
3. **Margin Filtering**: Automatically filter out running headers, footers, and page numbers by comparing with context pages.
{style_instruction}

### OUTPUT JSON SCHEMA:
You MUST respond with a valid JSON object matching this schema:
{{
  "markdown": "The full extracted markdown content of the target page",
  "document_metadata": {{
    "title": "Document title",
    "style_conformity": 0.0 to 1.0 score,
    "style_patch": null or {{ "new_rule": "..." }}
  }},
  "assets": [
    {{
      "id": "Unique asset ID (e.g., fig1)",
      "bbox": [ymin, xmin, ymax, xmax] normalized 0-1000,
      "caption": "Literal caption text",
      "description": "Short visual description"
    }}
  ]
}}
"""
