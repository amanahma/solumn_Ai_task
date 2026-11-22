"""
healthcheck.py — Pre-flight check for the load tester.  (COMPLETE — do not edit.)

Verifies that the target API is reachable and the results directory is writable
before the main run starts.  Called by controller.py before send_requests().
"""

from __future__ import annotations

import sys
import urllib.request
import urllib.error
from pathlib import Path


def check_target_reachable(url: str, timeout: float = 5.0) -> bool:
    """
    Return True if the target URL responds to a single GET within ``timeout``
    seconds, regardless of HTTP status code.  A connection error returns False.

    Parameters
    ----------
    url : str
        The URL to probe (e.g. "http://127.0.0.1:8000/api/check").
    timeout : float
        Socket timeout in seconds.
    """
    try:
        urllib.request.urlopen(url, timeout=timeout)
        return True
    except urllib.error.HTTPError:
        # HTTP error means the server is up — just returned a non-2xx status.
        return True
    except Exception:
        return False


def check_output_dir_writable(output_file: str) -> bool:
    """
    Return True if the directory that will hold ``output_file`` exists and
    is writable by the current process.

    Creates the directory (and any parents) if it does not already exist.

    Parameters
    ----------
    output_file : str
        Absolute path of the report file, e.g. "/app/results/report.json".
    """
    path = Path(output_file)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        # Write a zero-byte sentinel and immediately remove it.
        sentinel = path.parent / ".writable_check"
        sentinel.touch()
        sentinel.unlink()
        return True
    except OSError:
        return False


def run_preflight(target_url: str, output_file: str) -> None:
    """
    Run all pre-flight checks and exit with code 1 if any fail.

    Called automatically by controller.py before the load test begins.

    Parameters
    ----------
    target_url : str
        URL read from ``config.toml [load_test] target_url``.
    output_file : str
        Path read from ``config.toml [report] output_file``.
    """
    ok = True

    if not check_target_reachable(target_url):
        print(
            f"[preflight] FAIL — target not reachable: {target_url}",
            file=sys.stderr,
            flush=True,
        )
        ok = False
    else:
        print(f"[preflight] OK   — target reachable: {target_url}", flush=True)

    if not check_output_dir_writable(output_file):
        print(
            f"[preflight] FAIL — output directory not writable: {output_file}",
            file=sys.stderr,
            flush=True,
        )
        ok = False
    else:
        print(f"[preflight] OK   — output dir writable: {Path(output_file).parent}", flush=True)

    if not ok:
        sys.exit(1)
