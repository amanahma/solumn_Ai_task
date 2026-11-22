"""
depbot_runner.py - Main entry point for the depbot synchronization run.
(COMPLETE - do not edit.)

Loads configuration, invokes sync_package, and exits 0 on success.
"""
from __future__ import annotations
import os
import sys
import tomllib
from pathlib import Path

from updater import sync_package

CONFIG_PATH = Path(os.environ.get("CONFIG_PATH", "/app/config.toml"))
if not CONFIG_PATH.exists():
    CONFIG_PATH = Path(__file__).parent / "config.toml"


def load_config() -> dict:
    raw = CONFIG_PATH.read_bytes().lstrip(b"\xef\xbb\xbf")
    return tomllib.loads(raw.decode("utf-8"))


def main() -> int:
    cfg = load_config()
    package = cfg["sync"]["package"]
    version = cfg["sync"]["version"]
    mirror_url = cfg["mirror"]["url"]
    index_url = cfg["index"]["url"]
    cache_dir = os.environ.get("CACHE_DIR", cfg["mirror"]["cache_dir"])

    print(f"[runner] starting dependency sync: {package}=={version}", flush=True)
    success = sync_package(
        package=package,
        version=version,
        mirror_url=mirror_url,
        index_url=index_url,
        cache_dir=cache_dir,
    )

    if success:
        print("[runner] synchronization completed successfully", flush=True)
        return 0
    else:
        print("[runner] synchronization failed", file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
