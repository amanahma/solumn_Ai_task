"""
probe_logger.py - Audit logger for outbound network probes.
(COMPLETE - do not edit.)
"""
from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_LOG_PATH = Path(os.environ.get("PROBE_LOG_PATH", "/app/logs/probes.log"))


def log_probe(
    target: str,
    probe_type: str,
    status: str,
    detail: str = "",
    log_path: Path | None = None,
) -> None:
    """Append an audit record of a diagnostic probe.

    Parameters
    ----------
    target : str
        Target endpoint that was probed.
    probe_type : str
        Type of probe ("http", "traceroute").
    status : str
        Probe outcome status ("ok", "error", "skipped").
    detail : str, optional
        Additional probe detail.
    log_path : Path, optional
        Override destination log file.
    """
    p = log_path or DEFAULT_LOG_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "target": target,
        "probe_type": probe_type,
        "status": status,
        "detail": detail,
    }
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")
