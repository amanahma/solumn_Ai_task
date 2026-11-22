"""
solution/collector.py — Safe reference implementation.
Drop this into /app/collector.py to replace the stub.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class RequestResult:
    """Outcome of a single HTTP request."""
    status_code: int
    latency_ms: float
    timestamp: float


@dataclass
class Summary:
    """Aggregated statistics over a list of RequestResult objects."""
    total_requests: int
    status_codes: dict[str, int]
    rejection_rate: float
    latency_percentiles: dict[str, float]


def compute_summary(
    results: list[RequestResult],
    percentiles: list[int],
) -> Summary:
    """Aggregate request results into a Summary (nearest-rank percentiles)."""
    if not results:
        return Summary(
            total_requests=0,
            status_codes={},
            rejection_rate=0.0,
            latency_percentiles={f"p{p}": 0.0 for p in percentiles},
        )

    total = len(results)

    sc: dict[str, int] = {}
    for r in results:
        key = str(r.status_code)
        sc[key] = sc.get(key, 0) + 1

    rejected = sum(v for k, v in sc.items() if int(k) >= 400)
    rejection_rate = rejected / total

    latencies = sorted(r.latency_ms for r in results)
    lp: dict[str, float] = {}
    for p in percentiles:
        idx = max(0, min(math.ceil(p / 100 * total) - 1, total - 1))
        lp[f"p{p}"] = latencies[idx]

    return Summary(
        total_requests=total,
        status_codes=sc,
        rejection_rate=rejection_rate,
        latency_percentiles=lp,
    )
