# core/report_generator.py
import json
from typing import Dict, Any, List

def generate_report(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    summary = []
    for r in results:
        if "error" in r:
            summary.append(f"[{r['check']}] ❌ Error: {r['error']}")
        elif r["check"] == "bias":
            summary.append(f"[Bias] Score: {r.get('score', 'N/A')}")
        elif r["check"] == "safety":
            summary.append(f"[Safety] Category: {r.get('category', 'unknown')}")
        elif r["check"] == "hallucination":
            summary.append(f"[Hallucination] Issues: {len(r.get('issues', []))}")
        elif r["check"] == "policy":
            summary.append(f"[Policy] Violations: {len(r.get('violations', []))}")

    return {
        "summary": " | ".join(summary),
        "checks": results
    }

def print_report(report: Dict[str, Any]):
    print("\n===== Compliance Report =====")
    print(report["summary"])
    print(json.dumps(report, indent=2))
