"""
solution/sender.py — Safe reference implementation.
Drop this into /app/sender.py to replace the stub.
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
    Send exactly ``config.max_total_requests`` GET requests at
    ``config.max_rps``, throttled by TokenBucket.
    """
    bucket = TokenBucket(rate=config.max_rps)
    results: list[RequestResult] = []

    async with httpx.AsyncClient(timeout=config.timeout_seconds) as client:
        for _ in range(config.max_total_requests):
            await bucket.acquire()
            t_start = time.monotonic()
            wall = time.time()
            try:
                resp = await client.get(config.target_url)
                status = resp.status_code
            except Exception:
                status = 0
            latency = (time.monotonic() - t_start) * 1000.0
            results.append(RequestResult(
                status_code=status,
                latency_ms=latency,
                timestamp=wall,
            ))

    return results
