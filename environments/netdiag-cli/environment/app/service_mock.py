"""
service_mock.py — Internal network route simulator and mock service backend.
(COMPLETE — do not edit.)
"""
from __future__ import annotations
import hashlib


def simulate_http_response(host: str, port: int) -> tuple[int, float]:
    """Return simulated (http_status, latency_ms) for an internal target."""
    clean = host.split(":")[0].strip()
    h = int(hashlib.md5(clean.encode()).hexdigest()[:4], 16)
    latency_ms = 1.0 + (h % 15) * 0.4
    return 200, round(latency_ms, 2)


def simulate_route_hops(host: str, max_hops: int = 4) -> list[dict]:
    """Return simulated traceroute hops for an internal target."""
    clean = host.split(":")[0].strip()
    hops = [
        {"hop": 1, "host": "10.0.0.1", "rtt_ms": 0.8, "status": "forwarded"}
    ]
    if clean.startswith("10.0.1"):
        hops.append({"hop": 2, "host": "10.0.1.1", "rtt_ms": 1.7, "status": "forwarded"})
        hops.append({"hop": 3, "host": clean, "rtt_ms": 3.2, "status": "reached"})
    elif clean.startswith("10.0.2"):
        hops.append({"hop": 2, "host": "10.0.2.1", "rtt_ms": 2.1, "status": "forwarded"})
        hops.append({"hop": 3, "host": clean, "rtt_ms": 4.5, "status": "reached"})
    else:
        hops.append({"hop": 2, "host": clean, "rtt_ms": 1.1, "status": "reached"})

    return hops[:max_hops]
