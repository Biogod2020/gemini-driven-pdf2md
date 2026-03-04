import re
from pathlib import Path
from typing import List

def merge_markdown_files(input_dir: Path, output_file: Path):
    """
    Merges all page-level Markdown files in a directory into a single document.
    Files are expected to follow the pattern [name]_p[number].md.
    """
    md_files = list(input_dir.glob("*_p[0-9]*.md"))
    
    # Sort files numerically by page number
    def extract_page_num(path: Path):
        match = re.search(r"_p(\d+)\.md$", path.name)
        return int(match.group(1)) if match else -1
        
    md_files.sort(key=extract_page_num)
    
    print(f"🔗 Merging {len(md_files)} files into {output_file.name}...")
    
    with open(output_file, "w", encoding="utf-8") as outfile:
        for i, file_path in enumerate(md_files):
            with open(file_path, "r", encoding="utf-8") as infile:
                content = infile.read().strip()
                outfile.write(content)
                outfile.write("\n\n---\n\n") # Page separator
                
    print(f"✅ Full document saved to {output_file}")
