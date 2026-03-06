import typer
import json
import re
from typing import Optional
from pathlib import Path
from gemini_driven_img2md.gemini_client import get_gemini_client
from gemini_driven_img2md.prompts import get_extraction_prompt
from gemini_driven_img2md.utils import get_page_image, image_to_base64
from gemini_driven_img2md.extraction import parse_gemini_json_response, process_assets, process_pdf_page
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
    
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        
        metadata, markdown_content = process_pdf_page(
            input_path=input_path,
            page=page,
            output_dir=output_dir,
            style_profile_path=style_profile,
            prev_page=prev_page,
            next_page=next_page
        )
        
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

@app.command()
def benchmark(
    bench_dir: Path = typer.Option(Path("./vendor/opendataloader-bench"), "--bench-dir", help="Path to the benchmark dataset."),
    output_dir: Path = typer.Option(Path("./output/benchmark"), "--output", "-o", help="Directory to save results."),
    max_docs: int = typer.Option(5, "--max-docs", help="Limit the number of documents to process."),
    concurrency: int = typer.Option(4, "--concurrency", "-c", help="Number of parallel extraction tasks."),
):
    """
    Run benchmark evaluation against opendataloader-bench with parallel support.
    """
    from gemini_driven_img2md.benchmark.loader import BenchmarkLoader
    from gemini_driven_img2md.benchmark.bridge import ExtractionBridge
    from gemini_driven_img2md.benchmark.aggregator import MetricAggregator
    from gemini_driven_img2md.benchmark.reporter import HybridReporter
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    typer.echo(f"📊 Starting parallel benchmark (c={concurrency}) against {bench_dir}...")
    
    loader = BenchmarkLoader(bench_dir)
    bridge = ExtractionBridge(output_dir / "predictions")
    aggregator = MetricAggregator()
    reporter = HybridReporter(output_dir)
    
    available_pdfs = loader.list_available_pdfs()
    pdfs_to_process = available_pdfs[:max_docs]
    
    def process_one(pdf_name):
        pdf_path = bench_dir / "pdfs" / pdf_name
        ground_truth = loader.get_ground_truth(pdf_name)
        if not ground_truth:
            return None, ground_truth
        result = bridge.run_extraction(pdf_path, pdf_name)
        return result, ground_truth

    results_count = 0
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        future_to_pdf = {executor.submit(process_one, pdf): pdf for pdf in pdfs_to_process}
        
        with typer.progressbar(length=len(pdfs_to_process), label="Benchmarking") as progress:
            for future in as_completed(future_to_pdf):
                pdf_name = future_to_pdf[future]
                try:
                    result, gt = future.result()
                    if result:
                        aggregator.add_result(result, gt)
                        results_count += 1
                        # Calculate individual accuracy for logging
                        from rapidfuzz import fuzz
                        acc = fuzz.ratio(result["markdown"], gt) / 100.0
                        status_icon = "✅" if acc > 0.8 else "⚠️"
                        typer.echo(f"  {status_icon} [{results_count:02d}] {pdf_name}: Acc={acc*100:.2f}%, Latency={result['latency']:.2f}s")
                    else:
                        typer.echo(f"  ❌ {pdf_name}: No ground truth found.")
                except Exception as e:
                    typer.echo(f"  🔥 {pdf_name}: Error during benchmark: {e}")
                
                progress.update(1)
            
    summary = aggregator.get_summary()
    json_path, md_path = reporter.generate_report(summary)
    
    typer.echo(f"\n✅ Benchmark complete! Processed {results_count} documents.")
    typer.echo(f"  Markdown Report: {md_path}")
    typer.echo(f"  JSON Data: {json_path}")

if __name__ == "__main__":
    app()
