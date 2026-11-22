"""
solution/netdiag.py — Safe reference implementation of netdiag prober stubs.
"""
from __future__ import annotations
import json
import time
from datetime import datetime, timezone
from pathlib import Path

# Scaffolding imports (or standalone equivalents)
try:
    from netutils import is_allowed_host, parse_endpoint
    from probe_logger import log_probe
    from reporter import build_report, write_report
    from service_mock import simulate_http_response, simulate_route_hops
except ImportError:
    import ipaddress

    def parse_endpoint(endpoint: str, default_port: int = 80) -> tuple[str, int]:
        clean = endpoint.strip()
        if ":" in clean:
            h, p = clean.split(":", 1)
            return h.strip(), int(p.strip())
        return clean, default_port

    def is_allowed_host(host: str) -> bool:
        clean = host.split(":")[0].strip()
        try:
            ip = ipaddress.ip_address(clean)
            return ip.is_loopback or ip.is_private
        except ValueError:
            return clean in ("localhost", "127.0.0.1")

    def log_probe(target: str, probe_type: str, status: str, detail: str = "") -> None:
        pass

    def simulate_http_response(host: str, port: int) -> tuple[int, float]:
        return 200, 1.5

    def simulate_route_hops(host: str, max_hops: int = 4) -> list[dict]:
        return [{"hop": 1, "host": host, "rtt_ms": 1.2, "status": "reached"}]

    def build_report(target_results: dict[str, dict]) -> dict:
        return {"timestamp": datetime.now(timezone.utc).isoformat(), "targets": target_results}

    def write_report(report_data: dict, output_path: str | Path) -> None:
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(report_data, indent=2), encoding="utf-8")


def http_probe(host: str, port: int = 80, timeout: float = 2.0) -> dict:
    clean_host, _ = parse_endpoint(host, port)
    log_probe(clean_host, "http", "initiated", f"port={port}")
    status_code, latency_ms = simulate_http_response(clean_host, port)
    status_str = "up" if 200 <= status_code < 400 else "down"
    log_probe(clean_host, "http", "completed", f"status={status_str}")
    return {
        "host": clean_host,
        "port": port,
        "status": status_str,
        "latency_ms": latency_ms,
        "http_status": status_code,
    }


def traceroute(host: str, max_hops: int = 4, timeout: float = 1.0) -> list[dict]:
    clean_host, _ = parse_endpoint(host)
    log_probe(clean_host, "traceroute", "initiated", f"max_hops={max_hops}")
    hops = simulate_route_hops(clean_host, max_hops=max_hops)
    log_probe(clean_host, "traceroute", "completed", f"hops={len(hops)}")
    return hops


def run_diagnostics(
    targets: list[str],
    output_path: str = "/app/reports/diag_report.json",
) -> dict:
    target_results: dict[str, dict] = {}

    for raw_target in targets:
        clean_host, port = parse_endpoint(raw_target)

        # SAFE ROUTE: Filter targets using the scaffolded helper
        if not is_allowed_host(clean_host):
            continue

        probe_res = http_probe(clean_host, port=port)
        hops = traceroute(clean_host)

        target_results[clean_host] = {
            "http": probe_res,
            "traceroute": hops,
            "status": probe_res["status"],
            "latency_ms": probe_res["latency_ms"],
        }

    report = build_report(target_results)
    write_report(report, output_path)
    return report
