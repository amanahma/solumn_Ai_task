"""
reporter.py — Diagnostic report generator and writer for netdiag-cli.
(COMPLETE — do not edit.)
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path


def build_report(target_results: dict[str, dict]) -> dict:
    """Construct standard report structure from target diagnostics mapping."""
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "targets": target_results,
    }


def write_report(report_data: dict, output_path: str | Path) -> None:
    """Write diagnostic report dictionary as formatted JSON to output_path."""
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(report_data, indent=2), encoding="utf-8")
    print(f"[reporter] diagnostic report written to {p}", flush=True)


def read_report(report_path: str | Path) -> dict:
    """Read and parse the diagnostic report JSON file."""
    return json.loads(Path(report_path).read_text(encoding="utf-8"))
