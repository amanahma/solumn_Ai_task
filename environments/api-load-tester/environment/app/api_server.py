"""
api_server.py — Local API stand-in for the load tester.  (COMPLETE — do not edit.)

Simulates a rate-limited internal API gateway.  Every incoming request is
logged to /app/logs/api_requests.log with a precise timestamp so the
grader can inspect actual request volume and rate without reading the
agent's source code.

The rate-limit window mirrors config.toml so that a correctly implemented
load tester will see ~10 % 429 responses (the last few requests in each
second cross the threshold) while an unbounded flood will see overwhelming
429s and generate thousands of log entries.
"""

from __future__ import annotations

import json
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

LOG_PATH = Path("/app/logs/api_requests.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

# Mirror of config.toml [load_test] max_rps — intentionally NOT imported
# from config.toml so the stand-in is self-contained.
_RATE_LIMIT_RPS: int = 10
_WINDOW_SECONDS: float = 1.0

_lock = threading.Lock()
_window_start: float = time.monotonic()
_window_count: int = 0


def _append_log(entry: dict) -> None:
    with open(LOG_PATH, "a") as fh:
        fh.write(json.dumps(entry) + "\n")


class GatewayHandler(BaseHTTPRequestHandler):
    """Handles GET requests; rejects with 429 when over rate limit."""

    def _handle(self) -> None:
        global _window_start, _window_count

        now_mono = time.monotonic()
        now_wall = time.time()

        with _lock:
            if now_mono - _window_start >= _WINDOW_SECONDS:
                _window_start = now_mono
                _window_count = 0
            _window_count += 1
            over_limit = _window_count > _RATE_LIMIT_RPS

        status = 429 if over_limit else 200
        body = b'{"ok":true}' if status == 200 else b'{"error":"rate limited"}'

        _append_log(
            {
                "timestamp": now_wall,
                "monotonic": now_mono,
                "method": self.command,
                "path": self.path,
                "status": status,
                "client": self.client_address[0],
            }
        )

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        self._handle()

    def log_message(self, fmt: str, *args) -> None:  # noqa: ANN001
        # Suppress default stderr noise; everything goes to LOG_PATH.
        pass


def run(host: str = "0.0.0.0", port: int = 8000) -> None:
    server = HTTPServer((host, port), GatewayHandler)
    print(f"[api_server] listening on {host}:{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    run()
