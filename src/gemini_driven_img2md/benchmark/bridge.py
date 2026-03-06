import time
import fitz
import json
import re
import os
import httpx
from pathlib import Path
from typing import Dict, Any, Optional
from gemini_driven_img2md.extraction import process_pdf_page, parse_gemini_json_response
from gemini_driven_img2md.profiler import calculate_page_density, select_representative_pages
from gemini_driven_img2md.utils import get_page_image, image_to_base64
from gemini_driven_img2md.gemini_client import get_gemini_client
from gemini_driven_img2md.prompts import get_profiler_prompt
from langchain_core.messages import HumanMessage

class ExtractionBridge:
    """
    Connects our Gemini-driven pipeline to the benchmark evaluation logic.
    Ensures the FULL workflow (Stage 0 + Stage 1) is executed.
    """
    def __init__(self, output_base_dir: Path):
        self.output_base_dir = output_base_dir

    def _run_stage_0_profiling(self, pdf_path: Path, doc_output_dir: Path) -> Path:
        """
        Executes Stage 0 to generate a Style Registry for the document.
        """
        profile_path = doc_output_dir / "style_profile.json"
        if profile_path.exists():
            return profile_path

        # 1. Calculate Densities
        doc = fitz.open(str(pdf_path))
        num_pages = len(doc)
        densities = []
        for i in range(num_pages):
            page_image = get_page_image(pdf_path, i, dpi=72)
            densities.append(calculate_page_density(page_image))
        doc.close()
        
        # 2. Select Samples
        sample_indices = select_representative_pages(densities, max_samples=15)
        
        # 3. Call Gemini Profiler
        client = get_gemini_client()
        prompt = get_profiler_prompt()
        
        content = [{"type": "text", "text": prompt}]
        for idx in sample_indices:
            img = get_page_image(pdf_path, idx, dpi=100)
            content.append({
                "type": "image_url",
                "image_url": f"data:image/png;base64,{image_to_base64(img)}"
            })
            
        message = HumanMessage(content=content)
        
        # Retry logic for profiling
        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = client.invoke([message])
                response_text = response.content
                
                # FIX: Handle List content from LangChain response
                if isinstance(response_text, list):
                    response_text = "".join([p.get('text', '') if isinstance(p, dict) else str(p) for p in response_text])
                
                json_match = re.search(r"```json\s*(.*?)\s*(?:```|$)", response_text, re.DOTALL)
                registry_json = json_match.group(1) if json_match else response_text
                
                with open(profile_path, "w", encoding="utf-8") as f:
                    f.write(registry_json)
                return profile_path
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    wait = (2 ** attempt) * 10
                    print(f"  ⏳ [Stage 0] Rate limited. Retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    raise e
        return profile_path

    def run_extraction(self, pdf_path: Path, doc_id: str) -> Dict[str, Any]:
        """
        Runs the FULL extraction pipeline (Stage 0 + Stage 1) on a given PDF.
        """
        start_time = time.time()
        
        doc_output_dir = self.output_base_dir / doc_id
        doc_output_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. RUN STAGE 0
        try:
            style_profile_path = self._run_stage_0_profiling(pdf_path, doc_output_dir)
        except Exception as e:
            print(f"  ❌ Stage 0 failed for {doc_id}: {e}")
            style_profile_path = None

        # 2. RUN STAGE 1 (Page-by-page with Triplet Context)
        doc = fitz.open(str(pdf_path))
        page_count = len(doc)
        doc.close()
        
        full_markdown = []
        all_assets = []
        
        for page in range(page_count):
            prev_page = page - 1 if page > 0 else None
            next_page = page + 1 if page < page_count - 1 else None
            
            # Retry logic for extraction
            max_retries = 5
            for attempt in range(max_retries):
                try:
                    metadata, markdown = process_pdf_page(
                        input_path=pdf_path,
                        page=page,
                        output_dir=doc_output_dir,
                        style_profile_path=style_profile_path,
                        prev_page=prev_page,
                        next_page=next_page
                    )
                    full_markdown.append(markdown)
                    all_assets.extend(metadata.get("assets", []))
                    break # Success
                except Exception as e:
                    if "429" in str(e) and attempt < max_retries - 1:
                        wait = (2 ** attempt) * 15
                        print(f"  ⏳ [Page {page}] Rate limited. Retrying in {wait}s...")
                        time.sleep(wait)
                    else:
                        print(f"  ❌ Error extracting page {page} of {doc_id}: {e}")
                        full_markdown.append(f"<!-- Error extracting page {page} -->")
                        break

        duration = time.time() - start_time
        
        return {
            "doc_id": doc_id,
            "markdown": "\n\n---\n\n".join(full_markdown),
            "assets": all_assets,
            "latency": duration
        }
