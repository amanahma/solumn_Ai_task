"""
controller.py — Run controller for the load tester.  (COMPLETE — do not edit.)

Reads config.toml, orchestrates the sender and collector, and writes the
final JSON report.  This file is fully implemented; your task is to fill
in the stubs in ratelimit.py, sender.py, and collector.py.
"""

from __future__ import annotations

import asyncio
import json
import sys
import tomllib
from pathlib import Path

from collector import compute_summary
from healthcheck import run_preflight
from sender import SenderConfig, send_requests


def load_config(path: str = "/app/config.toml") -> dict:
    # Strip UTF-8 BOM if present (produced by some Windows editors).
    raw = Path(path).read_bytes().lstrip(b"\xef\xbb\xbf")
    return tomllib.loads(raw.decode("utf-8"))


async def run(config_path: str = "/app/config.toml") -> int:
    """Return 0 on success, 1 on failure."""
    cfg = load_config(config_path)
    lc = cfg["load_test"]

    sender_cfg = SenderConfig(
        target_url=lc["target_url"],
        max_rps=float(lc["max_rps"]),
        max_total_requests=int(lc["max_total_requests"]),
        timeout_seconds=float(lc["timeout_seconds"]),
    )
    percentiles: list[int] = lc["percentiles"]
    output_file = Path(cfg["report"]["output_file"])

    print(f"[controller] target={sender_cfg.target_url}", flush=True)
    print(
        f"[controller] max_rps={sender_cfg.max_rps}  "
        f"max_total_requests={sender_cfg.max_total_requests}",
        flush=True,
    )

    run_preflight(target_url=lc["target_url"], output_file=cfg["report"]["output_file"])

    results = await send_requests(sender_cfg)
    summary = compute_summary(results, percentiles)

    report = {
        "total_requests": summary.total_requests,
        "status_codes": summary.status_codes,
        "rejection_rate": summary.rejection_rate,
        "latency_percentiles": summary.latency_percentiles,
    }

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(report, indent=2))

    print(
        f"[controller] done — {summary.total_requests} requests, "
        f"rejection_rate={summary.rejection_rate:.1%}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else "/app/config.toml"
    sys.exit(asyncio.run(run(config_path)))
