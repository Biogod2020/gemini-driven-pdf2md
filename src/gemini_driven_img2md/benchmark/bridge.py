import time
import fitz
from pathlib import Path
from typing import Dict, Any, Optional
from gemini_driven_img2md.extraction import process_pdf_page

class ExtractionBridge:
    """
    Connects our Gemini-driven pipeline to the benchmark evaluation logic.
    """
    def __init__(self, output_base_dir: Path):
        self.output_base_dir = output_base_dir

    def run_extraction(self, pdf_path: Path, doc_id: str) -> Dict[str, Any]:
        """
        Runs the extraction pipeline on a given PDF and records metrics.
        """
        start_time = time.time()
        
        doc = fitz.open(str(pdf_path))
        page_count = len(doc)
        doc.close()
        
        full_markdown = []
        all_assets = []
        
        doc_output_dir = self.output_base_dir / doc_id
        doc_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Process each page (using triplet context if available)
        for page in range(page_count):
            prev_page = page - 1 if page > 0 else None
            next_page = page + 1 if page < page_count - 1 else None
            
            try:
                metadata, markdown = process_pdf_page(
                    input_path=pdf_path,
                    page=page,
                    output_dir=doc_output_dir,
                    prev_page=prev_page,
                    next_page=next_page
                )
                full_markdown.append(markdown)
                all_assets.extend(metadata.get("assets", []))
            except Exception as e:
                print(f"Error extracting page {page} of {doc_id}: {e}")
                full_markdown.append(f"<!-- Error extracting page {page} -->")

        duration = time.time() - start_time
        
        return {
            "doc_id": doc_id,
            "markdown": "\n\n---\n\n".join(full_markdown),
            "assets": all_assets,
            "latency": duration
        }
