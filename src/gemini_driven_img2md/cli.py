import typer
import json
import re
from typing import Optional
from pathlib import Path
from gemini_driven_img2md.gemini_client import get_gemini_client
from gemini_driven_img2md.prompts import get_extraction_prompt
from gemini_driven_img2md.utils import get_page_image, image_to_base64
from gemini_driven_img2md.extraction import parse_gemini_response, process_assets
from gemini_driven_img2md.profiler import calculate_page_density, select_representative_pages
from langchain_core.messages import HumanMessage
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

@app.command()
def extract(
    input_path: Path = typer.Argument(..., help="Path to the PDF or image document."),
    output_dir: Path = typer.Option(Path("./output"), "--output", "-o", help="Directory to save extracted content."),
    page: int = typer.Option(0, "--page", "-p", help="Target page number to extract (0-indexed)."),
    style_profile: Optional[Path] = typer.Option(None, "--style-profile", help="Path to the style_profile.json."),
    prev_page: Optional[int] = typer.Option(None, "--prev-page", help="Previous page index for context."),
    next_page: Optional[int] = typer.Option(None, "--next-page", help="Next page index for context."),
):
    """
    Extract content from a document and convert it to Markdown using Triplet Context.
    """
    if not input_path.exists():
        typer.echo(f"Error: File {input_path} does not exist.", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Processing {input_path} (Target: Page {page}, Context: {prev_page}, {next_page})...")
    
    # 1. Load Images
    try:
        # Load Target
        target_image = get_page_image(input_path, page)
        
        # Load Contexts
        prev_image = None
        if prev_page is not None:
            prev_image = get_page_image(input_path, prev_page)
            
        next_image = None
        if next_page is not None:
            next_image = get_page_image(input_path, next_page)
            
    except Exception as e:
        typer.echo(f"Error loading document pages: {e}", err=True)
        raise typer.Exit(code=1)

    # 2. Load Style Registry
    from gemini_driven_img2md.registry import StyleRegistryManager
    registry_mgr = StyleRegistryManager(style_profile)
    profile_data = registry_mgr.get_current_profile_json()

    # 3. Prepare Gemini call
    client = get_gemini_client()
    prompt = get_extraction_prompt(style_profile=profile_data)
    
    # Multimodal content list
    content = [{"type": "text", "text": prompt}]
    
    # Add Previous Page Context
    if prev_image:
        content.append({"type": "text", "text": "### [CONTEXT] PREVIOUS PAGE (Reference Only)"})
        content.append({
            "type": "image_url",
            "image_url": f"data:image/png;base64,{image_to_base64(prev_image)}"
        })
        
    # Add Target Page (The one to extract)
    content.append({"type": "text", "text": "### [TARGET] THE CURRENT PAGE TO EXTRACT"})
    content.append({
        "type": "image_url",
        "image_url": f"data:image/png;base64,{image_to_base64(target_image)}"
    })
    
    # Add Next Page Context
    if next_image:
        content.append({"type": "text", "text": "### [CONTEXT] NEXT PAGE (Reference Only)"})
        content.append({
            "type": "image_url",
            "image_url": f"data:image/png;base64,{image_to_base64(next_image)}"
        })
    
    message = HumanMessage(content=content)

    # 4. Call Gemini
    typer.echo("Calling Gemini API with Triplet Context...")
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

    # 5. Parse and Process
    try:
        metadata, markdown_content = parse_gemini_response(response_text)
        
        # Ensure asset IDs are unique across pages and sync Markdown text
        for asset in metadata.get("assets", []):
            old_id = asset.get("id")
            if old_id:
                new_id = f"p{page}_{old_id}"
                # 1. Update the ID in metadata for physical cropping
                asset["id"] = new_id
                # 2. Sync the Markdown content to use the new unique path
                # Replacing assets/old_id.png with assets/new_id.png
                old_path = f"assets/{old_id}.png"
                new_path = f"assets/{new_id}.png"
                markdown_content = markdown_content.replace(old_path, new_path)
        
        # Handle Style Evolution
        patch = metadata.get("document_metadata", {}).get("style_patch")
        if patch:
            typer.echo(f"  ✨ Style Patch detected! Updating registry...")
            registry_mgr.apply_patch(patch)
            if style_profile:
                registry_mgr.save(style_profile)
        
        conformity = metadata.get("document_metadata", {}).get("style_conformity", 1.0)
        if conformity < 0.7:
            typer.echo(f"  ⚠️ Low Style Conformity detected: {conformity}")

        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save assets and generate images.json
        process_assets(metadata, target_image, output_dir)
        
        # Save final Markdown
        output_md_path = output_dir / f"{input_path.stem}_p{page}.md"
        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
            
        typer.echo(f"Success! Output saved to {output_dir}")
        typer.echo(f"Markdown: {output_md_path.name}")
        
    except Exception as e:
        typer.echo(f"Error processing response: {e}", err=True)
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

@app.command()
def merge(
    input_dir: Path = typer.Argument(..., help="Directory containing page Markdown files."),
    output_name: str = typer.Option("full_document.md", "--output", "-o", help="Name of the combined Markdown file."),
):
    """
    Merge all page-level Markdown files into one.
    """
    from gemini_driven_img2md.merger import merge_markdown_files
    
    output_path = input_dir / output_name
    merge_markdown_files(input_dir, output_path)

if __name__ == "__main__":
    app()
