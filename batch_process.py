import os
import subprocess
from pathlib import Path
import fitz
from tqdm import tqdm
import time

def get_pdf_page_count(pdf_path: Path) -> int:
    doc = fitz.open(str(pdf_path))
    count = len(doc)
    doc.close()
    return count

def process_all_pdfs(resources_dir: Path, output_base_dir: Path):
    pdfs = list(resources_dir.glob("*.pdf"))
    print(f"🚀 Found {len(pdfs)} PDFs to process: {[p.name for p in pdfs]}")
    
    for pdf in pdfs:
        page_count = get_pdf_page_count(pdf)
        print(f"\n📄 Processing: {pdf.name} ({page_count} pages)")
        
        pdf_output_dir = output_base_dir / pdf.stem
        pdf_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Using tqdm for a progress bar
        for page in tqdm(range(page_count), desc=f"Progress: {pdf.name}", unit="page"):
            # Resuming logic
            output_md = pdf_output_dir / f"{pdf.stem}_p{page}.md"
            if output_md.exists():
                tqdm.write(f"  ⏭️ Page {page} already exists, skipping.")
                continue

            # 1. Extraction Step
            env = os.environ.copy()
            env["PYTHONPATH"] = f"{env.get('PYTHONPATH', '')}:{Path.cwd() / 'src'}"
            
            extract_cmd = [
                "/Users/jay/micromamba/envs/pdf_process/bin/python", "src/gemini_driven_img2md/cli.py",
                "extract", str(pdf),
                "--output", str(pdf_output_dir),
                "--page", str(page)
            ]
            
            start_time = time.time()
            result = subprocess.run(extract_cmd, env=env, capture_output=True, text=True)
            duration = time.time() - start_time
            
            if result.returncode == 0:
                tqdm.write(f"  ✅ Page {page} extracted in {duration:.2f}s")
                
                # Add a short delay after successful extraction to avoid 429
                time.sleep(10)
                
                # 2. Validation Step
                val_cmd = [
                    "/Users/jay/micromamba/envs/pdf_process/bin/python", "src/gemini_driven_img2md/cli.py",
                    "validate", str(pdf),
                    str(output_md),
                    str(pdf_output_dir / "images.json"),
                    "--page", str(page)
                ]
                
                val_start = time.time()
                val_result = subprocess.run(val_cmd, env=env, capture_output=True, text=True)
                val_duration = time.time() - val_start
                
                if val_result.returncode == 0:
                    report = val_result.stdout
                    status = "✅ PERFECT" if "PERFECT" in report.upper() else "⚠️ ISSUES"
                    tqdm.write(f"  🔍 Validation ({status}) in {val_duration:.2f}s")
                else:
                    tqdm.write(f"  ❌ Validation FAILED for Page {page}: {val_result.stderr}")
                
                # Add a longer cool-down between full page cycles
                time.sleep(15)
            else:
                if "429" in result.stderr:
                    tqdm.write(f"  ⏳ Rate limited (429) on Page {page}. Sleeping for 60s...")
                    time.sleep(60)
                else:
                    tqdm.write(f"  🔥 Extraction FAILED for Page {page}: {result.stderr}")
                # Optional: break or continue
                # break 

if __name__ == "__main__":
    resources = Path("resources")
    output = Path("output")
    process_all_pdfs(resources, output)
