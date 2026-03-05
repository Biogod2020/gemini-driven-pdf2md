import pytest
import json
from pathlib import Path
from gemini_driven_img2md.benchmark.loader import BenchmarkLoader

@pytest.fixture
def mock_bench_dir(tmp_path):
    # Create mock structure
    bench_dir = tmp_path / "bench"
    pdfs_dir = bench_dir / "pdfs"
    pdfs_dir.mkdir(parents=True)
    gt_dir = bench_dir / "ground-truth" / "markdown"
    gt_dir.mkdir(parents=True)
    
    # Create sample files
    (pdfs_dir / "test1.pdf").touch()
    with open(gt_dir / "test1.md", "w") as f:
        f.write("# Ground Truth")
        
    ref_data = {"test1.pdf": {"elements": []}}
    with open(bench_dir / "ground-truth" / "reference.json", "w") as f:
        json.dump(ref_data, f)
        
    return bench_dir

def test_benchmark_loader(mock_bench_dir):
    loader = BenchmarkLoader(mock_bench_dir)
    
    assert "test1.pdf" in loader.list_available_pdfs()
    assert loader.get_ground_truth("test1.pdf") == "# Ground Truth"
    assert loader.get_metadata("test1.pdf") == {"elements": []}
    
    assert loader.get_ground_truth("nonexistent.pdf") is None
    assert loader.get_metadata("nonexistent.pdf") is None
