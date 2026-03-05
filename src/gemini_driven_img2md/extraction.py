import json
import re
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from PIL import Image
from gemini_driven_img2md.utils import crop_image_normalized, get_page_image, image_to_base64
from gemini_driven_img2md.gemini_client import get_gemini_client
from gemini_driven_img2md.prompts import get_extraction_prompt
from gemini_driven_img2md.registry import StyleRegistryManager
from langchain_core.messages import HumanMessage

def parse_gemini_response(response_text: str) -> Tuple[Dict[str, Any], str]:
    """
    Parses the dual-section response from Gemini.
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
    remaining_text = response_text[json_match.end():].strip()
    remaining_text = re.sub(r"^\s*---\s*", "", remaining_text)
    markdown_content = re.sub(r"\s*---\s*$", "", remaining_text).strip()

    if not markdown_content:
        parts = response_text.split("---")
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
            final_id = asset_id
            output_path = assets_dir / f"{final_id}.png"
            crop_image_normalized(page_image, bbox, output_path)
            
            asset_entry = {
                "id": final_id,
                "path": str(output_path.relative_to(output_dir)),
                "caption": asset.get("caption"),
                "description": asset.get("description")
            }
            new_assets.append(asset_entry)
    
    existing_paths = {a["path"] for a in current_index}
    for na in new_assets:
        if na["path"] not in existing_paths:
            current_index.append(na)
    
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(current_index, f, indent=2, ensure_ascii=False)
    
    return new_assets

def process_pdf_page(
    input_path: Path,
    page: int,
    output_dir: Path,
    style_profile_path: Optional[Path] = None,
    prev_page: Optional[int] = None,
    next_page: Optional[int] = None,
) -> Tuple[Dict[str, Any], str]:
    """
    Core extraction logic for a single PDF page.
    """
    # 1. Load Images
    target_image = get_page_image(input_path, page)
    prev_image = get_page_image(input_path, prev_page) if prev_page is not None else None
    next_image = get_page_image(input_path, next_page) if next_page is not None else None

    # 2. Load Style Registry
    registry_mgr = StyleRegistryManager(style_profile_path)
    profile_data = registry_mgr.get_current_profile_json()

    # 3. Prepare Gemini call
    client = get_gemini_client()
    prompt = get_extraction_prompt(style_profile=profile_data)
    
    content = [{"type": "text", "text": prompt}]
    if prev_image:
        content.append({"type": "text", "text": "### [CONTEXT] PREVIOUS PAGE (Reference Only)"})
        content.append({"type": "image_url", "image_url": f"data:image/png;base64,{image_to_base64(prev_image)}"})
        
    content.append({"type": "text", "text": "### [TARGET] THE CURRENT PAGE TO EXTRACT"})
    content.append({"type": "image_url", "image_url": f"data:image/png;base64,{image_to_base64(target_image)}"})
    
    if next_image:
        content.append({"type": "text", "text": "### [CONTEXT] NEXT PAGE (Reference Only)"})
        content.append({"type": "image_url", "image_url": f"data:image/png;base64,{image_to_base64(next_image)}"})
    
    message = HumanMessage(content=content)

    # 4. Call Gemini
    response = client.invoke([message])
    response_text = response.content

    # 5. Parse and Process
    metadata, markdown_content = parse_gemini_response(response_text)
    
    # Ensure unique asset IDs
    for asset in metadata.get("assets", []):
        old_id = asset.get("id")
        if old_id:
            new_id = f"p{page}_{old_id}"
            asset["id"] = new_id
            markdown_content = markdown_content.replace(f"assets/{old_id}.png", f"assets/{new_id}.png")
    
    # Handle Style Evolution
    patch = metadata.get("document_metadata", {}).get("style_patch")
    if patch:
        registry_mgr.apply_patch(patch)
        if style_profile_path:
            registry_mgr.save(style_profile_path)
            
    # Save assets
    process_assets(metadata, target_image, output_dir)
    
    return metadata, markdown_content
