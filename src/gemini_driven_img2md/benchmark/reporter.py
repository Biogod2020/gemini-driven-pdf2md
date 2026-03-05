import json
from pathlib import Path
from typing import Dict, Any

class HybridReporter:
    """
    Generates benchmark reports in Markdown and JSON formats.
    """
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_report(self, summary: Dict[str, Any]):
        """
        Writes the reports to the output directory.
        """
        # 1. JSON Report
        json_path = self.output_dir / "results.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
            
        # 2. Markdown Report
        md_path = self.output_dir / "report.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# Benchmark Evaluation Report\n\n")
            f.write(f"## Overall Metrics\n")
            f.write(f"- **Total Documents**: {summary.get('total_documents')}\n")
            f.write(f"- **Average Latency**: {summary.get('average_latency'):.2f}s\n")
            f.write(f"- **Average Accuracy**: {summary.get('average_accuracy')*100:.2f}%\n\n")
            
            f.write("## Individual Results\n")
            f.write("| Doc ID | Accuracy | Latency | Assets |\n")
            f.write("|--------|----------|---------|--------|\n")
            for res in summary.get("results", []):
                f.write(f"| {res['doc_id']} | {res['accuracy']*100:.2f}% | {res['latency']:.2f}s | {res['assets_count']} |\n")
                
        return json_path, md_path
