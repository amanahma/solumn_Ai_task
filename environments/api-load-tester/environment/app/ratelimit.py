"""
ratelimit.py — Token-bucket rate limiter for the load tester.
"""

import asyncio
import time


class TokenBucket:
    """
    Async token-bucket rate limiter.

    Tokens are added to the bucket at a fixed rate and consumed on each
    call to acquire(). If the bucket is empty, acquire() waits until a
    token becomes available before returning.

    Parameters
    ----------
    rate : float
        Maximum sustained throughput in tokens per second.
    """

    def __init__(self, rate: float) -> None:
        if rate <= 0:
            raise ValueError("rate must be positive")
        self.rate: float = rate
        self._tokens: float = rate
        self._last_refill: float = time.monotonic()
        self._lock: asyncio.Lock = asyncio.Lock()

    async def acquire(self) -> None:
        """
        Wait until a token is available, then consume it.

        TODO: implement the refill-and-wait logic.
        """
        raise NotImplementedError(
            "Implement token-refill logic and sleep-until-token-available"
        )
