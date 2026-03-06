import os
import asyncio
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from gemini_driven_img2md.extraction import process_pdf_page
from gemini_driven_img2md.cli import profile as profile_func
from gemini_driven_img2md.merger import merge_markdown_files

# Create a FastMCP server
mcp = FastMCP("gemini-driven-img2md")

@mcp.tool()
async def profile_document(pdf_path: str, output_dir: str = "./output/mcp_profile"):
    """
    Stage 0: Analyze a PDF document to generate a Global Style Registry.
    
    Args:
        pdf_path: Path to the local PDF file.
        output_dir: Directory to save the style profile.
    """
    from gemini_driven_img2md.profiler import run_profiling
    path = Path(pdf_path)
    out = Path(output_dir)
    
    profile_path = run_profiling(path, out)
    
    return f"Style profiling complete for {pdf_path}. Registry saved to {profile_path}."

@mcp.tool()
async def extract_page(
    pdf_path: str, 
    page: int, 
    output_dir: str = "./output/mcp_extraction",
    style_profile: str = None,
    prev_page: int = None,
    next_page: int = None
):
    """
    Stage 1: Reconstruct a single page from a PDF with triplet context.
    
    Args:
        pdf_path: Path to the local PDF file.
        page: The target page number (0-indexed).
        output_dir: Directory to save extracted content.
        style_profile: Optional path to a style_profile.json.
        prev_page: Optional previous page for context.
        next_page: Optional next page for context.
    """
    path = Path(pdf_path)
    out = Path(output_dir)
    profile_path = Path(style_profile) if style_profile else None
    
    metadata, markdown = process_pdf_page(
        input_path=path,
        page=page,
        output_dir=out,
        style_profile_path=profile_path,
        prev_page=prev_page,
        next_page=next_page
    )
    
    return {
        "metadata": metadata,
        "markdown": markdown,
        "assets_path": str(out / "assets")
    }

if __name__ == "__main__":
    mcp.run()
