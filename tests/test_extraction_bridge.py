import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from gemini_driven_img2md.benchmark.bridge import ExtractionBridge

def test_extraction_bridge_init(tmp_path):
    bridge = ExtractionBridge(tmp_path)
    assert bridge.output_base_dir == tmp_path

@patch("gemini_driven_img2md.benchmark.bridge.process_pdf_page")
@patch("fitz.open")
def test_run_extraction(mock_fitz, mock_process, tmp_path):
    bridge = ExtractionBridge(tmp_path)
    
    # Mock PDF page count
    mock_doc = MagicMock()
    mock_doc.__len__.return_value = 1
    mock_fitz.return_value = mock_doc
    
    # Mock extraction result
    mock_process.return_value = ({"title": "Test"}, "# Extracted")
    
    pdf_path = tmp_path / "test.pdf"
    pdf_path.touch()
    
    result = bridge.run_extraction(pdf_path, "test_id")
    
    assert result["doc_id"] == "test_id"
    assert result["markdown"] == "# Extracted"
    assert "latency" in result
