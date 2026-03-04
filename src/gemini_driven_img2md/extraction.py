import json
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
from PIL import Image
from gemini_driven_img2md.utils import crop_image_normalized

def parse_gemini_response(response_text: str) -> Tuple[Dict[str, Any], str]:
    """
    Parses the dual-section response from Gemini.
    Expected format is flexible but usually:
    ---
    ```json
    { ... }
    ```
    ---
    Markdown content
    ---
    """
    # 1. Find the JSON block
    json_match = re.search(r"```json\s*(.*?)\s*```", response_text, re.DOTALL)
    if not json_match:
        raise ValueError("Could not find JSON metadata block in Gemini response.")
    
    try:
        metadata = json.loads(json_match.group(1))
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON metadata: {e}")

    # 2. Extract Markdown content
    # The prompt asks for:
    # ---
    # JSON
    # ---
    # Markdown
    # ---
    
    # We look for the Markdown content after the closing ``` of the JSON block.
    # We also need to handle the potential trailing ---
    
    remaining_text = response_text[json_match.end():].strip()
    
    # Remove leading --- if present
    remaining_text = re.sub(r"^\s*---\s*", "", remaining_text)
    
    # Remove trailing --- if present (usually at the very end)
    markdown_content = re.sub(r"\s*---\s*$", "", remaining_text).strip()

    if not markdown_content:
        # If still empty, maybe it's between two --- after the JSON
        parts = response_text.split("---")
        # Try to find a part that is not JSON and not empty
        for part in parts:
            part = part.strip()
            if part and not part.startswith("```json"):
                markdown_content = part
                break

    return metadata, markdown_content

def process_assets(metadata: Dict[str, Any], page_image: Image.Image, output_dir: Path):
    """
    Crops and saves all identified assets from the page image, appending to the global index.
    """
    assets_dir = output_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    index_path = output_dir / "images.json"
    
    # Load existing index if it exists
    current_index = []
    if index_path.exists():
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                current_index = json.load(f)
        except Exception:
            current_index = []

    new_assets = []
    for asset in metadata.get("assets", []):
        asset_id = asset.get("id")
        bbox = asset.get("bbox")
        if asset_id and bbox:
            # Ensure unique ID by checking current_index
            final_id = asset_id
            # If ID already exists, it might be a multi-page table or same ID used by model
            # We skip if it's identical path or modify ID
            output_path = assets_dir / f"{final_id}.png"
            
            # Simple check to avoid redundant cropping of same file
            # though usually each page's assets are unique
            crop_image_normalized(page_image, bbox, output_path)
            
            asset_entry = {
                "id": final_id,
                "path": str(output_path.relative_to(output_dir)),
                "caption": asset.get("caption"),
                "description": asset.get("description")
            }
            
            # Update or append
            # For simplicity, we append. In SOTA, we should deduplicate.
            new_assets.append(asset_entry)
    
    # Merge new assets into current index (avoid duplicates based on ID and Path)
    existing_paths = {a["path"] for a in current_index}
    for na in new_assets:
        if na["path"] not in existing_paths:
            current_index.append(na)
    
    # Save the updated cumulative images.json
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(current_index, f, indent=2, ensure_ascii=False)
    
    return new_assets
