"""
collector.py — Aggregate raw request results into summary statistics.

Consumed by controller.py after send_requests() returns.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class RequestResult:
    """Outcome of a single HTTP request."""

    status_code: int        # HTTP status (0 on connection error)
    latency_ms: float       # Round-trip time in milliseconds
    timestamp: float        # Unix wall-clock time at request start


@dataclass
class Summary:
    """Aggregated statistics over a list of RequestResult objects."""

    total_requests: int
    status_codes: dict[str, int]           # str(status_code) → count
    rejection_rate: float                  # fraction of responses with status >= 400, in [0, 1]
    latency_percentiles: dict[str, float]  # "p50" → ms, "p90" → ms, …


def compute_summary(
    results: list[RequestResult],
    percentiles: list[int],
) -> Summary:
    """
    Build a Summary from a completed list of RequestResult objects.

    Parameters
    ----------
    results : list[RequestResult]
        One entry per request, as returned by send_requests().
    percentiles : list[int]
        Percentile ranks to compute (e.g. [50, 90, 95, 99]).
        Each becomes a key "p<N>" in Summary.latency_percentiles.

    Returns
    -------
    Summary
        Populated with:
        - total_requests     : number of entries in results
        - status_codes       : {str(status_code): count, …}
        - rejection_rate     : count(status >= 400) / total; 0.0 if total == 0
        - latency_percentiles: {"p50": <ms>, "p90": <ms>, …}
          Use nearest-rank method: index = ceil(p/100 * n) - 1 (0-based).

    TODO: implement this function.
    """
    raise NotImplementedError("Implement summary aggregation")
