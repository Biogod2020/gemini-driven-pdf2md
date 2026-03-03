import pytest
import json
from pathlib import Path
from PIL import Image
from gemini_driven_img2md.extraction import parse_gemini_response, process_assets

def test_parse_gemini_response():
    sample_response = """
---
```json
{
  "document_metadata": {"title": "Test"},
  "assets": [{"id": "fig1", "bbox": [100, 100, 200, 200]}]
}
```
---
# Hello World
This is a test.
---
"""
    metadata, markdown = parse_gemini_response(sample_response)
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
