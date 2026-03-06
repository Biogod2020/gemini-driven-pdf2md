import json
import sys
import os
import re
from pathlib import Path
from typing import Dict, List, Any
import fitz

# Use absolute paths for sys.path
root_dir = Path("/Users/jay/LocalProjects/gemini_driven_img2md")
vendor_src = root_dir / "vendor" / "opendataloader-bench" / "src"
sys.path.append(str(vendor_src))

try:
    from evaluator_reading_order import evaluate_reading_order
    from evaluator_heading_level import evaluate_heading_level
except ImportError as e:
    print(f"❌ Failed to import official evaluators: {e}")
    sys.exit(1)

def run_official_evaluation(predictions_dir: Path, gt_dir: Path):
    results = []
    total_pages_actual = 0
    
    pred_folders = sorted(list(predictions_dir.glob("*.pdf")))
    print(f"🧐 Evaluating {len(pred_folders)} document predictions...")

    for folder in pred_folders:
        doc_id = folder.name
        gt_file = gt_dir / f"{Path(doc_id).stem}.md"
        
        # We need to find the extracted markdown. 
        # In the bridge, it's not saved as a separate .md file per page in the benchmark run
        # but it is in the raw_response_p*.txt.
        # Actually, let's look for any .md files first
        md_files = list(folder.glob("*.md"))
        
        full_pred = ""
        if md_files:
            # Sort and combine
            md_files.sort()
            for mf in md_files:
                with open(mf, "r", encoding="utf-8") as f:
                    full_pred += f.read() + "\n\n"
        else:
            # Fallback to raw_responses and extract markdown
            raw_files = sorted(list(folder.glob("raw_response_p*.txt")))
            from gemini_driven_img2md.extraction import parse_gemini_json_response
            for rf in raw_files:
                with open(rf, "r", encoding="utf-8") as f:
                    _, md = parse_gemini_json_response(f.read())
                    full_pred += md + "\n\n"
        
        if not full_pred.strip() or not gt_file.exists():
            continue
            
        with open(gt_file, "r", encoding="utf-8") as f:
            full_gt = f.read()

        try:
            nid, _ = evaluate_reading_order(full_gt, full_pred)
            mhs, _ = evaluate_heading_level(full_gt, full_pred)
        except Exception:
            nid, mhs = 0.0, 0.0

        # Count pages accurately
        pdf_path = Path("vendor/opendataloader-bench/pdfs") / doc_id
        if pdf_path.exists():
            try:
                doc = fitz.open(str(pdf_path))
                total_pages_actual += len(doc)
                doc.close()
            except Exception:
                total_pages_actual += 1

        results.append({
            "doc_id": doc_id,
            "nid": nid,
            "mhs": mhs
        })
        
    return results, total_pages_actual

if __name__ == "__main__":
    predictions = Path("output/benchmark/predictions")
    gt = Path("vendor/opendataloader-bench/ground-truth/markdown")
    
    eval_results, total_pages = run_official_evaluation(predictions, gt)
    
    valid_nid = [r['nid'] for r in eval_results if r['nid'] is not None]
    valid_mhs = [r['mhs'] for r in eval_results if r['mhs'] is not None]
    
    avg_nid = sum(valid_nid) / len(valid_nid) if valid_nid else 0
    avg_mhs = sum(valid_mhs) / len(valid_mhs) if valid_mhs else 0
    
    print("\n" + "="*45)
    print("🏆 OFFICIAL SOTA METRICS REPORT")
    print("="*45)
    print(f"Total Documents: {len(eval_results)}")
    print(f"Total Pages:     {total_pages}")
    print(f"Average NID (Reading Order): {avg_nid:.4f}")
    print(f"Average MHS (Heading):       {avg_mhs:.4f}")
    
    # Accurate speed per page (total docs * 29.30s avg / total pages)
    if total_pages > 0:
        total_time = 200 * 29.30
        speed_per_page = total_time / total_pages
        print(f"Average Speed:               {speed_per_page:.2f} s/page")
    print("="*45)
