import pytest
import json
from pathlib import Path
from PIL import Image
from gemini_driven_img2md.extraction import parse_gemini_json_response, process_assets

def test_parse_gemini_response():
    sample_response = """
---
```json
{
  "markdown": "# Hello World\nThis is a test.",
  "document_metadata": {"title": "Test"},
  "assets": [{"id": "fig1", "bbox": [100, 100, 200, 200]}]
}
```
---
"""
    metadata, markdown = parse_gemini_json_response(sample_response)
    assert metadata["document_metadata"]["title"] == "Test"
    assert "fig1" in metadata["assets"][0]["id"]
    assert "# Hello World" in markdown
    assert "This is a test." in markdown

def test_process_assets(tmp_path):
    img = Image.new("RGB", (1000, 1000), color="blue")
    metadata = {
        "assets": [
            {"id": "test_fig", "bbox": [100, 100, 200, 200], "caption": "Test Caption"}
        ]
    }
    
    results = process_assets(metadata, img, tmp_path)
    
    assert (tmp_path / "assets" / "test_fig.png").exists()
    assert (tmp_path / "images.json").exists()
    
    with open(tmp_path / "images.json", "r") as f:
        saved_json = json.load(f)
        assert len(saved_json) == 1
        assert saved_json[0]["id"] == "test_fig"
        assert saved_json[0]["path"] == "assets/test_fig.png"

def test_parse_gemini_response_stress():
    """Stress test the parser with malformed inputs."""
    
    # 1. Truncated JSON
    truncated = """
```json
{
  "document_metadata": {"title": "Truncated"},
  "assets": [{"id": "fig1"
---
# Content
"""
    metadata, markdown = parse_gemini_json_response(truncated)
    assert metadata["document_metadata"]["title"] == "Truncated"
    # In JSON mode, markdown is inside the JSON. If JSON is truncated, 
    # the parser might return the raw text as markdown.
    assert "# Content" in markdown or "Truncated" in str(metadata)

    # 2. No JSON markers
    no_markers = '{"markdown": "# Content", "title": "No Markers"}'
    metadata, markdown = parse_gemini_json_response(no_markers)
    assert "# Content" in markdown

    # 3. Multiple JSON blocks (take first)
    multiple = """
```json
{"markdown": "# First", "id": "first"}
```
```json
{"markdown": "# Second", "id": "second"}
```
"""
    metadata, markdown = parse_gemini_json_response(multiple)
    assert metadata["id"] == "first"
    assert "# First" in markdown

    # 4. JSON as list
    list_json = """
```json
[{"id": "asset1"}]
```
# Content
"""
    metadata, markdown = parse_gemini_json_response(list_json)
    assert metadata["assets"][0]["id"] == "asset1"
    assert "# Content" in markdown
