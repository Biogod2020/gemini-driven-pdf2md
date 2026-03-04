def get_profiler_prompt() -> str:
    """
    Returns the Stage 0 prompt for generating a Global Style Registry.
    """
    return """
You are a Document Style Architect. Your task is to analyze the provided set of representative pages from a document and generate a **Global Style Registry** in JSON format.

### Your Analysis Goals:
1.  **Heading Weights**: Identify visual patterns for H1 through H6.
2.  **Visual Matchers**: Identify recurring structural elements (Sidebars, Code, Warnings).
3.  **Markdown Grammar**: Define how Math, Tables, and Citations should be formatted.
4.  **Layout Patterns**: Detect multi-column flows and identify "Margin Noise" (running headers, footers, page numbers).

### Required JSON Output Format:
```json
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
```
"""

def get_extraction_prompt(style_profile: str = "") -> str:
    """
    Returns the SOTA-level system prompt for high-fidelity document extraction.
    
    Args:
        style_profile: Optional JSON string containing the global style registry.
    """
    style_instruction = ""
    if style_profile:
        style_instruction = f"\n### GLOBAL STYLE REGISTRY:\nUse the following project-specific rules for this document:\n{style_profile}\n"

    return f"""
You are a SOTA Multimodal Document Intelligence Engine. Your mission is to perform high-fidelity, structural transformation of the provided document into a unified, standard Markdown format.

### TRIPLET CONTEXT INSTRUCTIONS:
You will receive up to three images labeled as:
1. **PREVIOUS PAGE**: (Reference Only) Use this to resolve cross-page paragraph breaks or list continuity.
2. **TARGET PAGE**: (PRIMARY EXTRACTION TARGET) This is the only page you will extract content from.
3. **NEXT PAGE**: (Reference Only) Use this to verify if tables, equations, or paragraphs continue beyond the target page.

### 1. MISSION CRITICAL RULES:
- **Target-Only Extraction**: Your output MUST contain content ONLY from the **TARGET PAGE**. Do not include content from the Previous or Next pages.
- **Strict Margin & Noise Filtering**: 
    1. Identify running headers, footers, and page numbers by comparing the triplet. 
    2. Any text that appears in the same coordinate region across PREVIOUS, TARGET, and NEXT pages is visual noise. 
    3. EXCLUDE these from the Markdown. No page numbers, no repeated titles.
- **Semantic Stitching**: Use the Previous Page to determine if the first paragraph of the Target Page is a continuation. If it is, ensure the text flow is seamless without a new header.
- **Literal Extraction**: Transcribe text EXACTLY as written. No paraphrasing.
- **Visual Layout Inference**: Handle multi-column text flows.
{style_instruction}
### 2. MATHEMATICAL NOTATION:
- Convert ALL mathematical expressions to LaTeX ($ for inline, $$ for blocks).

### 3. TABULAR DATA:
- **Format**: Use standard Markdown tables for simple grids.
- **Complexity Fallback**: If a table contains merged cells (colspan/rowspan) or nested structures, you MUST output it as a **well-formatted HTML <table>** within the Markdown to preserve structural integrity.

### 4. MULTIMODAL ASSET EXTRACTION:
For every figure/chart in the **TARGET PAGE**:
1. Identify the region and provide normalized coordinates `[ymin, xmin, ymax, xmax]` (0-1000).
2. Extract the literal caption.
3. Insert `![caption](assets/asset_id.png)` in the Markdown.

### 5. STYLE EVOLUTION (SOTA):
- **Style Conformity**: Rate how well the current page adheres to the Global Style Registry on a scale of 0.0 to 1.0.
- **Style Patch**: If you detect a NEW visual style or evolution, provide a JSON "patch" object to update the registry.

### 6. OUTPUT PROTOCOL:
Respond with:
---
```json
{{
  "document_metadata": {{ 
    "title": "...", 
    "style_conformity": 0.0-1.0,
    "style_patch": null or {{ "new_rule": "..." }}
  }},
  "assets": [ {{ "id": "...", "bbox": [...], "caption": "..." }} ]
}}
```
---
{{Markdown content for TARGET PAGE only}}
---
"""
