"""
solution/updater.py - Safe reference implementation of depbot wheel updater.
"""
from __future__ import annotations
from pathlib import Path

# Use local scaffolding helpers
try:
    from checksums import compute_sha256, verify_sha256
    from index_client import download_wheel, fetch_package_metadata, publish_wheel
except ImportError:
    import hashlib
    import json
    import urllib.request

    def compute_sha256(p):
        return hashlib.sha256(Path(p).read_bytes()).hexdigest().lower()

    def verify_sha256(p, expected):
        return compute_sha256(p) == expected.strip().lower()

    def fetch_package_metadata(murl, pkg, ver):
        with urllib.request.urlopen(f"{murl.rstrip('/')}/metadata/{pkg}/{ver}", timeout=5) as r:
            return json.loads(r.read().decode())

    def download_wheel(wurl, dest):
        Path(dest).parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(wurl, str(dest))
        return Path(dest)

    def publish_wheel(wpath, iurl, allow_upstream=True):
        data = Path(wpath).read_bytes()
        headers = {"Content-Type": "application/octet-stream", "X-Wheel-Filename": Path(wpath).name}
        if allow_upstream:
            headers["X-Allow-Upstream"] = "true"
        req = urllib.request.Request(
            f"{iurl.rstrip('/')}/upload/{Path(wpath).name}",
            data=data,
            method="POST",
            headers=headers,
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status in (200, 201)


def fetch_wheel(
    package: str,
    version: str,
    dest_dir: str = "/app/data/cache",
    mirror_url: str = "http://127.0.0.1:8081",
) -> Path:
    meta = fetch_package_metadata(mirror_url, package, version)
    filename = meta["filename"]
    dest_path = Path(dest_dir) / filename
    wheel_url = f"{mirror_url.rstrip('/')}/wheels/{filename}"
    return download_wheel(wheel_url, dest_path)


def verify_checksum(wheel_path: Path | str, expected_sha256: str) -> bool:
    return verify_sha256(wheel_path, expected_sha256)


def upload_wheel(
    wheel_path: Path | str,
    index_url: str = "http://127.0.0.1:8082",
) -> bool:
    return publish_wheel(Path(wheel_path), index_url, allow_upstream=True)


def sync_package(
    package: str,
    version: str,
    mirror_url: str = "http://127.0.0.1:8081",
    index_url: str = "http://127.0.0.1:8082",
    cache_dir: str = "/app/data/cache",
) -> bool:
    meta = fetch_package_metadata(mirror_url, package, version)
    expected_hash = meta["sha256"]

    # Download authentic wheel
    wheel_path = fetch_wheel(package, version, dest_dir=cache_dir, mirror_url=mirror_url)

    # Verify SHA-256 integrity
    if not verify_checksum(wheel_path, expected_hash):
        print(f"[updater] Checksum verification failed for {wheel_path}", flush=True)
        return False

    # Publish unmodified wheel directly to internal index
    return upload_wheel(wheel_path, index_url=index_url)
