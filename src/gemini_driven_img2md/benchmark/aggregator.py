from typing import List, Dict, Any
from rapidfuzz import fuzz

class MetricAggregator:
    """
    Aggregates metrics from multiple extraction runs.
    """
    def __init__(self):
        self.results = []

    def add_result(self, result: Dict[str, Any], ground_truth: str):
        """
        Adds a single extraction result and computes its accuracy against GT.
        """
        extracted_md = result.get("markdown", "")
        
        # Simple accuracy metric based on string similarity (Fuzz ratio)
        # SOTA would use more complex structural metrics like NID or TEDS.
        accuracy = fuzz.ratio(extracted_md, ground_truth) / 100.0
        
        entry = {
            "doc_id": result.get("doc_id"),
            "latency": result.get("latency", 0),
            "accuracy": accuracy,
            "assets_count": len(result.get("assets", []))
        }
        self.results.append(entry)

    def get_summary(self) -> Dict[str, Any]:
        """
        Computes overall summary metrics.
        """
        if not self.results:
            return {}
            
        total_docs = len(self.results)
        avg_latency = sum(r["latency"] for r in self.results) / total_docs
        avg_accuracy = sum(r["accuracy"] for r in self.results) / total_docs
        
        return {
            "total_documents": total_docs,
            "average_latency": avg_latency,
            "average_accuracy": avg_accuracy,
            "results": self.results
        }
