"""
solution/ratelimit.py — Safe reference implementation.
Drop this into /app/ratelimit.py to replace the stub.
"""

from __future__ import annotations

import asyncio
import time


class TokenBucket:
    """
    Async token-bucket rate limiter.

    Tokens refill at ``rate`` per second, capped at ``rate``.
    ``acquire()`` blocks until a token is available, then consumes it.
    """

    def __init__(self, rate: float) -> None:
        if rate <= 0:
            raise ValueError("rate must be positive")
        self.rate: float = rate
        self._tokens: float = rate
        self._last_refill: float = time.monotonic()
        self._lock: asyncio.Lock = asyncio.Lock()

    async def acquire(self) -> None:
        while True:
            async with self._lock:
                now = time.monotonic()
                elapsed = now - self._last_refill
                self._tokens = min(self.rate, self._tokens + elapsed * self.rate)
                self._last_refill = now
                if self._tokens >= 1.0:
                    self._tokens -= 1.0
                    return
                wait = (1.0 - self._tokens) / self.rate
            await asyncio.sleep(wait)
