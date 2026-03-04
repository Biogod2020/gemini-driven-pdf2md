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
        # 1. Stage 0: Global Style Profiling
        profile_dir = output_base_dir / pdf.stem
        profile_dir.mkdir(parents=True, exist_ok=True)
        style_profile_path = profile_dir / "style_profile.json"
        
        if not style_profile_path.exists():
            print(f"🎨 Generating Style Profile for {pdf.name}...")
            prof_cmd = [
                "/Users/jay/micromamba/envs/pdf_process/bin/python", "src/gemini_driven_img2md/cli.py",
                "profile", str(pdf),
                "--output", str(profile_dir)
            ]
            env = os.environ.copy()
            env["PYTHONPATH"] = f"{env.get('PYTHONPATH', '')}:{Path.cwd() / 'src'}"
            env["NO_PROXY"] = "localhost,127.0.0.1"
            subprocess.run(prof_cmd, env=env)
            # Cooling down after heavy profile request
            time.sleep(20)

        # 2. Stage 1: Triplet Extraction
        page_count = get_pdf_page_count(pdf)
        print(f"\n📄 Processing Content: {pdf.name} ({page_count} pages)")
        
        pdf_output_dir = output_base_dir / pdf.stem
        
        for page in tqdm(range(page_count), desc=f"Progress: {pdf.name}", unit="page"):
            output_md = pdf_output_dir / f"{pdf.stem}_p{page}.md"
            if output_md.exists():
                # tqdm.write(f"  ⏭️ Page {page} already exists, skipping.")
                continue

            # Context selection [N-1, N, N+1]
            prev_page = page - 1 if page > 0 else None
            next_page = page + 1 if page < page_count - 1 else None
            
            extract_cmd = [
                "/Users/jay/micromamba/envs/pdf_process/bin/python", "src/gemini_driven_img2md/cli.py",
                "extract", str(pdf),
                "--output", str(pdf_output_dir),
                "--page", str(page),
                "--style-profile", str(style_profile_path)
            ]
            if prev_page is not None:
                extract_cmd.extend(["--prev-page", str(prev_page)])
            if next_page is not None:
                extract_cmd.extend(["--next-page", str(next_page)])
            
            env = os.environ.copy()
            env["PYTHONPATH"] = f"{env.get('PYTHONPATH', '')}:{Path.cwd() / 'src'}"
            env["NO_PROXY"] = "localhost,127.0.0.1"
            
            start_time = time.time()
            result = subprocess.run(extract_cmd, env=env, capture_output=True, text=True)
            duration = time.time() - start_time
            
            if result.returncode == 0:
                tqdm.write(f"  ✅ Page {page} extracted in {duration:.2f}s")
                # Wait to avoid 429
                time.sleep(15)
            else:
                if "429" in result.stderr:
                    tqdm.write(f"  ⏳ Rate limited (429) on Page {page}. Sleeping for 60s...")
                    time.sleep(60)
                else:
                    tqdm.write(f"  🔥 Extraction FAILED for Page {page}: {result.stderr}")
                    # Optional: retry once
                    time.sleep(30)
        
        # After finishing each PDF, we can log the final evolved registry path
        tqdm.write(f"🏁 Finished {pdf.name}. Evolved registry: {style_profile_path}")
        
        # 3. Merge Phase
        tqdm.write(f"🔗 Merging pages for {pdf.name}...")
        merge_cmd = [
            "/Users/jay/micromamba/envs/pdf_process/bin/python", "src/gemini_driven_img2md/cli.py",
            "merge", str(pdf_output_dir)
        ]
        subprocess.run(merge_cmd, env=env)

if __name__ == "__main__":
    resources = Path("resources")
    output = Path("output")
    process_all_pdfs(resources, output)
