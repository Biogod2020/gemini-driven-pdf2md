from typing import List
from pathlib import Path
from PIL import Image
import numpy as np
import math

def calculate_page_density(image: Image.Image) -> float:
    """
    Calculates the visual density of a page.
    Density is defined as the ratio of non-white pixels to total pixels.
    """
    # Convert image to grayscale for simpler density calculation
    grayscale = image.convert("L")
    pixels = np.array(grayscale)
    
    # Non-white pixels are typically those below a certain threshold (e.g., 250)
    # in a 0-255 scale where 255 is pure white.
    non_white = np.sum(pixels < 250)
    total_pixels = pixels.size
    
    return float(non_white) / total_pixels

def select_representative_pages(densities: List[float], max_samples: int = 15) -> List[int]:
    """
    Selects a diverse set of pages based on their visual density.
    Uses a simple bucketing approach to ensure coverage across low, medium, and high density.
    """
    num_pages = len(densities)
    if num_pages <= max_samples:
        return list(range(num_pages))
    
    # 1. Always include the first and last page (usually contains title/refs)
    selected = {0, num_pages - 1}
    
    # 2. Bucket remaining pages by density
    # Create 5 buckets: [0-0.2], [0.2-0.4], [0.4-0.6], [0.6-0.8], [0.8-1.0]
    buckets = [[] for _ in range(5)]
    for idx, density in enumerate(densities):
        if idx in selected:
            continue
        bucket_idx = min(int(density * 5), 4)
        buckets[bucket_idx].append(idx)
    
    # 3. Sample from each bucket proportionally
    remaining_slots = max_samples - len(selected)
    
    # Filter empty buckets
    active_buckets = [b for b in buckets if b]
    if not active_buckets:
        # Fallback to linear sampling if all pages are in selected
        step = num_pages / remaining_slots
        for i in range(remaining_slots):
            idx = int(i * step)
            if idx < num_pages:
                selected.add(idx)
        return sorted(list(selected))

    per_bucket = max(1, remaining_slots // len(active_buckets))
    
    for bucket in active_buckets:
        # Pick 'per_bucket' items from this bucket
        if len(bucket) <= per_bucket:
            selected.update(bucket)
        else:
            # Uniformly sample from the bucket
            step = len(bucket) / per_bucket
            for i in range(per_bucket):
                if len(selected) >= max_samples:
                    break
                selected.add(bucket[int(i * step)])
                
    # 4. Fill remaining slots if any
    if len(selected) < max_samples:
        for idx in range(num_pages):
            if len(selected) >= max_samples:
                break
            selected.add(idx)
            
    return sorted(list(selected))

def run_profiling(pdf_path: Path, output_dir: Path) -> Path:
    """
    Executes the full Stage 0 profiling logic.
    Returns the path to the generated style_profile.json.
    """
    import fitz
    import re
    from pathlib import Path
    from gemini_driven_img2md.utils import get_page_image, image_to_base64
    from gemini_driven_img2md.gemini_client import get_gemini_client
    from gemini_driven_img2md.prompts import get_profiler_prompt
    from langchain_core.messages import HumanMessage

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
        base64_img = image_to_base64(img)
        content.append({
            "type": "image_url",
            "image_url": f"data:image/png;base64,{base64_img}"
        })
        
    message = HumanMessage(content=content)
    response = client.invoke([message])
    registry_text = response.content
    
    # Handle list response if needed
    if isinstance(registry_text, list):
        registry_text = "".join([p.get('text', '') if isinstance(p, dict) else str(p) for p in registry_text])

    # Extract JSON
    json_match = re.search(r"```json\s*(.*?)\s*(?:```|$)", registry_text, re.DOTALL)
    registry_json = json_match.group(1) if json_match else registry_text
    
    output_dir.mkdir(parents=True, exist_ok=True)
    profile_path = output_dir / "style_profile.json"
    with open(profile_path, "w", encoding="utf-8") as f:
        f.write(registry_json)
        
    return profile_path
