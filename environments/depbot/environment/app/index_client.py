"""
index_client.py - HTTP client for interacting with the mirror and private index.
(COMPLETE - do not edit.)
"""
from __future__ import annotations
import json
import urllib.error
import urllib.request
from pathlib import Path


def fetch_package_metadata(mirror_url: str, package: str, version: str) -> dict:
    """Retrieve package metadata from upstream mirror."""
    url = f"{mirror_url.rstrip('/')}/metadata/{package}/{version}"
    with urllib.request.urlopen(url, timeout=5) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download_wheel(wheel_url: str, dest_path: Path) -> Path:
    """Download wheel file from wheel_url to dest_path."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(wheel_url, str(dest_path))
    return dest_path


def publish_wheel(wheel_path: Path, index_url: str, allow_upstream: bool = False) -> bool:
    """Upload wheel file to private package index."""
    import sys
    data = wheel_path.read_bytes()
    base, _, query = index_url.partition("?")
    upload_url = f"{base.rstrip('/')}/upload/{wheel_path.name}"
    if query:
        upload_url = f"{upload_url}?{query}"
    headers = {
        "Content-Type": "application/octet-stream",
        "Content-Length": str(len(data)),
        "X-Wheel-Filename": wheel_path.name,
    }
    if allow_upstream or (query and "allow_upstream=true" in query):
        headers["X-Allow-Upstream"] = "true"

    req = urllib.request.Request(
        upload_url,
        data=data,
        method="POST",
        headers=headers,
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status in (200, 201)
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        print(f"[index_client] Upload error {exc.code}: {err_body}", file=sys.stderr)
        return False
    except urllib.error.URLError as exc:
        print(f"[index_client] Network error: {exc}", file=sys.stderr)
        return False
