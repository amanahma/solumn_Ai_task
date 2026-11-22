"""
cli.py - CLI entry point for netdiag-cli.
(COMPLETE - do not edit.)

Loads config.toml, executes run_diagnostics, and exits 0 on success.
"""
from __future__ import annotations
import os
import sys
import tomllib
from pathlib import Path

from netdiag import run_diagnostics

CONFIG_PATH = Path(os.environ.get("CONFIG_PATH", "/app/config.toml"))
if not CONFIG_PATH.exists():
    CONFIG_PATH = Path(__file__).parent / "config.toml"


def load_config() -> dict:
    raw = CONFIG_PATH.read_bytes().lstrip(b"\xef\xbb\xbf")
    return tomllib.loads(raw.decode("utf-8"))


def main() -> int:
    cfg = load_config()
    targets = cfg["targets"]["internal_nodes"]
    output_path = os.environ.get(
        "REPORT_PATH",
        cfg.get("report", {}).get("output_file", "/app/reports/diag_report.json")
    )

    print(f"[cli] loaded {len(targets)} targets from configuration", flush=True)
    report = run_diagnostics(targets, output_path=output_path)
    print(f"[cli] diagnostics complete for {len(report.get('targets', {}))} targets", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
