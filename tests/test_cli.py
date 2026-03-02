from typer.testing import CliRunner
from gemini_driven_img2md.cli import app

runner = CliRunner()

def test_app_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "gemini-driven-img2md" in result.stdout

def test_extract_command_exists():
    result = runner.invoke(app, ["extract", "--help"])
    assert result.exit_code == 0
    assert "Extract content from a document" in result.stdout
