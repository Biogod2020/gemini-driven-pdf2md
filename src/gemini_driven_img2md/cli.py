import typer
import json
import re
from typing import Optional
from pathlib import Path
from gemini_driven_img2md.gemini_client import get_gemini_client
from gemini_driven_img2md.prompts import get_extraction_prompt
from gemini_driven_img2md.utils import get_page_image
from gemini_driven_img2md.extraction import parse_gemini_response, process_assets
from gemini_driven_img2md.profiler import calculate_page_density, select_representative_pages
from langchain_core.messages import HumanMessage
import base64
from io import BytesIO
from PIL import Image

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

def image_to_base64(image, max_size=(1024, 1024)):
    # Resize image if it exceeds max_size to avoid 502/timeout issues
    img_copy = image.copy()
    img_copy.thumbnail(max_size, Image.Resampling.LANCZOS)
    buffered = BytesIO()
    img_copy.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

@app.command()
def extract(
    input_path: Path = typer.Argument(..., help="Path to the PDF or image document."),
    output_dir: Path = typer.Option(Path("./output"), "--output", "-o", help="Directory to save extracted content."),
    page: int = typer.Option(0, "--page", "-p", help="Page number to extract (0-indexed)."),
):
    """
    Extract content from a document and convert it to Markdown.
    """
    if not input_path.exists():
        typer.echo(f"Error: File {input_path} does not exist.", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Processing {input_path} (page {page})...")
    
    # 1. Load the page as an image
    try:
        if input_path.suffix.lower() == ".pdf":
            page_image = get_page_image(input_path, page)
        else:
            from PIL import Image
            page_image = Image.open(input_path).convert("RGB")
    except Exception as e:
        typer.echo(f"Error loading document: {e}", err=True)
        raise typer.Exit(code=1)

    # 2. Prepare Gemini call
    client = get_gemini_client()
    prompt = get_extraction_prompt()
    
    # Encode image for multimodal input
    base64_image = image_to_base64(page_image)
    
    # ChatGoogleGenerativeAI expects a specific content list format
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": f"data:image/png;base64,{base64_image}",
            },
        ]
    )

    # 3. Call Gemini
    typer.echo("Calling Gemini API...")
    try:
        response = client.invoke([message])
        response_text = response.content
        
        # DEBUG: Always save raw response
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(output_dir / f"raw_response_p{page}.txt", "w", encoding="utf-8") as f:
            f.write(response_text)
            
    except Exception as e:
        typer.echo(f"Error calling Gemini API: {e}", err=True)
        raise typer.Exit(code=1)

    # 4. Parse and Process
    try:
        metadata, markdown_content = parse_gemini_response(response_text)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save assets and generate images.json
        process_assets(metadata, page_image, output_dir)
        
        # Save final Markdown
        output_md_path = output_dir / f"{input_path.stem}_p{page}.md"
        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
            
        typer.echo(f"Success! Output saved to {output_dir}")
        typer.echo(f"Markdown: {output_md_path.name}")
        
    except Exception as e:
        typer.echo(f"Error processing response: {e}", err=True)
        # Still save the raw response for debugging
        debug_path = output_dir / "raw_response.txt"
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(response_text)
        typer.echo(f"Raw response saved to {debug_path} for debugging.")
        raise typer.Exit(code=1)

@app.command()
def profile(
    input_path: Path = typer.Argument(..., help="Path to the PDF document."),
    output_dir: Path = typer.Option(Path("./output"), "--output", "-o", help="Directory to save the style profile."),
):
    """
    Stage 0: Analyze the document to generate a Global Style Registry.
    """
    from gemini_driven_img2md.prompts import get_profiler_prompt
    import fitz
    
    if not input_path.exists() or input_path.suffix.lower() != ".pdf":
        typer.echo(f"Error: {input_path} is not a valid PDF file.", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"🚀 Starting Style Profiling for {input_path.name}...")
    
    # 1. Calculate Densities
    doc = fitz.open(str(input_path))
    num_pages = len(doc)
    densities = []
    
    typer.echo(f"  📊 Scanning {num_pages} pages for visual density...")
    with typer.progressbar(range(num_pages), label="Scanning") as progress:
        for i in progress:
            page_image = get_page_image(input_path, i, dpi=72) # Low res for speed
            densities.append(calculate_page_density(page_image))
    
    # 2. Select Samples
    sample_indices = select_representative_pages(densities, max_samples=15)
    typer.echo(f"  🎯 Selected {len(sample_indices)} representative pages: {sample_indices}")
    
    # 3. Call Gemini Profiler
    client = get_gemini_client()
    prompt = get_profiler_prompt()
    
    content = [{"type": "text", "text": prompt}]
    for idx in sample_indices:
        img = get_page_image(input_path, idx, dpi=100) # Medium res for AI analysis
        base64_img = image_to_base64(img)
        content.append({
            "type": "image_url",
            "image_url": f"data:image/png;base64,{base64_img}"
        })
        
    message = HumanMessage(content=content)
    
    typer.echo("  🧠 Generating Global Style Registry...")
    try:
        response = client.invoke([message])
        registry_text = response.content
        
        # Extract JSON from response (handling markdown blocks)
        json_match = re.search(r"```json\s*(.*?)\s*```", registry_text, re.DOTALL)
        if json_match:
            registry_json = json_match.group(1)
        else:
            registry_json = registry_text
            
        output_dir.mkdir(parents=True, exist_ok=True)
        profile_path = output_dir / "style_profile.json"
        
        with open(profile_path, "w", encoding="utf-8") as f:
            f.write(registry_json)
            
        typer.echo(f"  ✅ Style Registry saved to {profile_path}")
        
    except Exception as e:
        typer.echo(f"  ❌ Profiling failed: {e}", err=True)
        raise typer.Exit(code=1)

@app.command()
def validate(
    original_path: Path = typer.Argument(..., help="Path to the original document."),
    markdown_path: Path = typer.Argument(..., help="Path to the generated Markdown file."),
    assets_json: Path = typer.Argument(..., help="Path to the generated images.json."),
    page: int = typer.Option(0, "--page", "-p", help="Page number of the original document."),
):
    """
    Validate the conversion quality using Gemini.
    """
    from gemini_driven_img2md.validator import validate_conversion
    
    typer.echo(f"Validating {markdown_path} against {original_path} (page {page})...")
    
    try:
        if original_path.suffix.lower() == ".pdf":
            page_image = get_page_image(original_path, page)
        else:
            from PIL import Image
            page_image = Image.open(original_path).convert("RGB")
            
        report = validate_conversion(page_image, markdown_path, assets_json)
        typer.echo("\n--- VALIDATION REPORT ---")
        typer.echo(report)
        typer.echo("--------------------------")
        
    except Exception as e:
        typer.echo(f"Error during validation: {e}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
