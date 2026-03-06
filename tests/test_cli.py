from typer.testing import CliRunner
from gemini_driven_img2md.cli import app
from unittest.mock import patch, MagicMock
from pathlib import Path
from PIL import Image

runner = CliRunner()

def test_app_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "gemini-driven-img2md" in result.stdout

def test_extract_command_help():
    result = runner.invoke(app, ["extract", "--help"])
    assert result.exit_code == 0
    assert "Extract content from a document" in result.stdout

@patch("gemini_driven_img2md.extraction.get_gemini_client")
@patch("gemini_driven_img2md.extraction.get_page_image")
def test_extract_flow(mock_get_page, mock_get_client, tmp_path):
    # Mocking dependencies
    mock_image = MagicMock(spec=Image.Image)
    mock_image.size = (1000, 1000)
    mock_get_page.return_value = mock_image
    
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    
    mock_response = MagicMock()
    # Updated mock response to match JSON mode output
    mock_response.content = """
{
  "markdown": "# Test Content\\n![Figure 1](assets/fig1.png)",
  "document_metadata": {"title": "Test Paper"},
  "assets": [{"id": "fig1", "bbox": [100, 100, 200, 200], "caption": "Figure 1"}]
}
"""
    mock_client.invoke.return_value = mock_response
    
    # Run extract command
    dummy_pdf = tmp_path / "test.pdf"
    dummy_pdf.touch()
    
    output_dir = tmp_path / "output"
    
    # Note: process_pdf_page is imported in extraction.py and used in cli.py
    # We might need to mock it where it's used if direct mocking fails
    result = runner.invoke(app, ["extract", str(dummy_pdf), "--output", str(output_dir)])
    
    if result.exit_code != 0:
        print(result.stdout)
        print(result.stderr)
    
    assert result.exit_code == 0
    assert "Success" in result.stdout
    # The file name will be test_p0.md
    assert (output_dir / "test_p0.md").exists()
    assert (output_dir / "images.json").exists()

@patch("gemini_driven_img2md.cli.get_gemini_client")
@patch("gemini_driven_img2md.cli.get_page_image")
@patch("fitz.open")
def test_profile_command(mock_fitz, mock_get_page, mock_get_client, tmp_path):
    # Mocking
    mock_doc = MagicMock()
    mock_doc.__len__.return_value = 5
    mock_fitz.return_value = mock_doc
    
    mock_image = Image.new("RGB", (100, 100), color="white")
    mock_get_page.return_value = mock_image
    
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.content = '```json\n{"heading_weights": {}}\n```'
    mock_client.invoke.return_value = mock_response
    
    dummy_pdf = tmp_path / "test.pdf"
    dummy_pdf.touch()
    
    result = runner.invoke(app, ["profile", str(dummy_pdf), "--output", str(tmp_path)])
    
    if result.exit_code != 0:
        print(result.stdout)
        print(result.stderr)
        
    assert result.exit_code == 0
    assert "Style Registry saved" in result.stdout
    assert (tmp_path / "style_profile.json").exists()
