import json
import re
import os
import httpx
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from PIL import Image
from json_repair import repair_json
from gemini_driven_img2md.utils import crop_image_normalized, get_page_image, image_to_base64
from gemini_driven_img2md.gemini_client import get_gemini_client
from gemini_driven_img2md.prompts import get_extraction_prompt, get_profiler_prompt
from gemini_driven_img2md.registry import StyleRegistryManager
from langchain_core.messages import HumanMessage

def parse_gemini_json_response(response_text: str) -> Tuple[Dict[str, Any], str]:
    """
    Parses the response when response_mime_type is application/json.
    Expected format is a single JSON object with 'markdown', 'document_metadata', and 'assets'.
    """
    try:
        # 1. Extract potential JSON content
        json_content = response_text
        json_start_marker = "```json"
        json_end_marker = "```"
        
        if json_start_marker in response_text:
            # Find the first json block for metadata
            match = re.search(r"```json\s*(.*?)\s*(?:```|$)", response_text, re.DOTALL)
            if match:
                json_content = match.group(1).strip()
        
        repaired_json = repair_json(json_content.strip())
        data = json.loads(repaired_json)
        
        if isinstance(data, list):
            data = {"assets": data}
            
        if not isinstance(data, dict):
            return {"assets": []}, str(data)
            
        markdown = data.get("markdown", "")
        
        # 2. Robust Markdown Recovery
        # If markdown is empty inside JSON, or if there are other parts of the response,
        # we try to collect all text that is NOT inside any ```json block.
        if not markdown.strip() or len(markdown) < 10:
            # Find all json blocks and remove them from the raw text
            clean_text = response_text
            all_json_matches = list(re.finditer(r"```json\s*(.*?)\s*(?:```|$)", response_text, re.DOTALL))
            
            # Remove from end to start to preserve indices
            for m in reversed(all_json_matches):
                clean_text = clean_text[:m.start()] + "\n" + clean_text[m.end():]
            
            outside_md = clean_text.strip()
            if len(outside_md) > len(markdown):
                markdown = outside_md
        
        # Remove the markdown field from metadata to keep it clean
        metadata = {k: v for k, v in data.items() if k != "markdown"}
        
        # 3. Final Cleanup
        # Remove leftover markdown markers if any
        markdown = markdown.replace("```json", "").replace("```", "").strip()
        markdown = re.sub(r"^\s*---\s*", "", markdown, flags=re.MULTILINE)
        markdown = re.sub(r"\s*---\s*$", "", markdown, flags=re.MULTILINE).strip()
        
        return metadata, markdown
    except Exception as e:
        return {"assets": [], "error": str(e)}, response_text

def process_assets(metadata: Dict[str, Any], page_image: Image.Image, output_dir: Path):
    """
    Crops and saves all identified assets from the page image.
    """
    assets_dir = output_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    index_path = output_dir / "images.json"
    
    current_index = []
    if index_path.exists():
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                current_index = json.load(f)
        except Exception: pass

    new_assets = []
    if isinstance(metadata, dict):
        for asset in metadata.get("assets", []):
            asset_id = asset.get("id")
            bbox = asset.get("bbox")
            if asset_id and bbox:
                output_path = assets_dir / f"{asset_id}.png"
                try:
                    crop_image_normalized(page_image, bbox, output_path)
                    new_assets.append({
                        "id": asset_id,
                        "path": str(output_path.relative_to(output_dir)),
                        "caption": asset.get("caption"),
                        "description": asset.get("description")
                    })
                except Exception: pass
    
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
    Core extraction logic using OFFICIAL Structured Output (JSON Mode).
    """
    # 1. Load Images
    target_image = get_page_image(input_path, page)
    prev_image = get_page_image(input_path, prev_page) if prev_page is not None else None
    next_image = get_page_image(input_path, next_page) if next_page is not None else None

    # 2. Prepare Prompt
    registry_mgr = StyleRegistryManager(style_profile_path)
    profile_data = registry_mgr.get_current_profile_json()
    prompt = get_extraction_prompt(style_profile=profile_data)

    # 3. Construct NATIVE Gemini Payload with JSON Mode
    user_parts = []
    if prev_image:
        user_parts.append({"text": "### [CONTEXT] PREVIOUS PAGE"})
        user_parts.append({"inlineData": {"mimeType": "image/png", "data": image_to_base64(prev_image)}})
        
    user_parts.append({"text": "### [TARGET] THE CURRENT PAGE TO EXTRACT"})
    user_parts.append({"inlineData": {"mimeType": "image/png", "data": image_to_base64(target_image)}})
    
    if next_image:
        user_parts.append({"text": "### [CONTEXT] NEXT PAGE"})
        user_parts.append({"inlineData": {"mimeType": "image/png", "data": image_to_base64(next_image)}})

    payload = {
        "systemInstruction": {
            "parts": [{"text": prompt}]
        },
        "contents": [
            {"role": "user", "parts": user_parts}
        ],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    # 4. API Call with RECITATION handling
    api_endpoint = os.getenv("GEMINI_API_ENDPOINT", "http://localhost:8888")
    api_key = os.getenv("GEMINI_API_KEY", "123456")
    model = "gemini-3-flash-preview"
    url = f"{api_endpoint}/v1beta/models/{model}:generateContent"
    
    headers = {"x-goog-api-key": api_key, "Content-Type": "application/json"}
    response_text = ""
    
    for attempt in [0.0, 1.0]:
        payload["generationConfig"]["temperature"] = attempt
        try:
            with httpx.Client(proxies={}, timeout=180.0) as client:
                resp = client.post(url, headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    candidate = data['candidates'][0]
                    if candidate.get('finishReason') == 'RECITATION' and attempt == 0.0:
                        continue
                    
                    try:
                        parts = candidate['content']['parts']
                        response_text = "".join([p['text'] for p in parts if 'text' in p])
                        break
                    except (KeyError, IndexError):
                        response_text = str(data)
                        break
                else:
                    response_text = f"API Error {resp.status_code}: {resp.text}"
                    break
        except Exception as e:
            response_text = f"Request Exception: {str(e)}"
            break

    # Always save raw response
    with open(output_dir / f"raw_response_p{page}.txt", "w", encoding="utf-8") as f:
        f.write(response_text)

    # 5. Parse JSON-based response
    metadata, markdown_content = parse_gemini_json_response(response_text)
    
    if isinstance(metadata, dict):
        assets = metadata.get("assets", [])
        for asset in assets:
            if "id" in asset:
                old_id = asset["id"]
                new_id = f"p{page}_{old_id}"
                asset["id"] = new_id
                markdown_content = markdown_content.replace(f"assets/{old_id}.png", f"assets/{new_id}.png")
        
        doc_meta = metadata.get("document_metadata", {})
        if isinstance(doc_meta, dict):
            patch = doc_meta.get("style_patch")
            if patch:
                registry_mgr.apply_patch(patch)
                if style_profile_path: registry_mgr.save(style_profile_path)
            
    process_assets(metadata, target_image, output_dir)
    return metadata, markdown_content
