import typer
from typing import Optional
from pathlib import Path

app = typer.Typer(name="gemini-driven-img2md", help="A tool to convert research paper PDFs to Markdown using Gemini vision.")

def version_callback(value: bool):
    if value:
        typer.echo("gemini-driven-img2md version 0.1.0")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True, help="Show the version and exit."
    ),
):
    """
    Multimodal document extraction tool powered by Gemini.
    """
    pass

@app.command()
def extract(
    input_path: Path = typer.Argument(..., help="Path to the PDF or image document."),
    output_dir: Path = typer.Option(Path("./output"), "--output", "-o", help="Directory to save extracted content."),
):
    """
    Extract content from a document and convert it to Markdown.
    """
    typer.echo(f"Extracting from {input_path} to {output_dir}...")
    # TODO: Implement extraction logic in Phase 2/3

if __name__ == "__main__":
    app()
