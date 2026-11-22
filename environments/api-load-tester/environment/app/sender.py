"""
sender.py — HTTP request sender for the load tester.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import httpx

from collector import RequestResult
from ratelimit import TokenBucket


@dataclass
class SenderConfig:
    """Runtime parameters for a single load-test run."""

    target_url: str
    max_rps: float
    max_total_requests: int
    timeout_seconds: float = 5.0


async def send_requests(config: SenderConfig) -> list[RequestResult]:
    """
    Send requests to config.target_url and return results for the collector.

    For each request, record status_code, latency_ms, and timestamp.
    On connection error, set status_code to 0.

    Returns a list[RequestResult], one entry per request sent.
    """
    raise NotImplementedError("Implement the request sending loop")
