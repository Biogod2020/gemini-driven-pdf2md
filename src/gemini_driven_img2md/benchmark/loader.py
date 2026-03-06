import json
from pathlib import Path
from typing import Dict, List, Optional

class BenchmarkLoader:
    """
    Loads data from the opendataloader-bench dataset.
    """
    def __init__(self, bench_dir: Path):
        self.bench_dir = bench_dir
        self.pdfs_dir = bench_dir / "pdfs"
        self.gt_dir = bench_dir / "ground-truth" / "markdown"
        self.reference_path = bench_dir / "ground-truth" / "reference.json"
        self.reference_data = {}
        
        if self.reference_path.exists():
            with open(self.reference_path, "r", encoding="utf-8") as f:
                self.reference_data = json.load(f)

    def list_available_pdfs(self) -> List[str]:
        """Returns a list of PDF filenames available in the benchmark, sorted alphabetically."""
        return sorted([p.name for p in self.pdfs_dir.glob("*.pdf")])

    def get_ground_truth(self, pdf_filename: str) -> Optional[str]:
        """Returns the ground truth markdown for a given PDF."""
        # GT files usually match the PDF name stem
        stem = Path(pdf_filename).stem
        gt_path = self.gt_dir / f"{stem}.md"
        if gt_path.exists():
            with open(gt_path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    def get_metadata(self, pdf_filename: str) -> Optional[Dict]:
        """Returns metadata (elements, boxes) for a given PDF from reference.json."""
        return self.reference_data.get(pdf_filename)
