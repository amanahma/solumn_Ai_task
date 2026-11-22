"""
updater.py - Wheel synchronization logic for depbot.
"""
from __future__ import annotations
from pathlib import Path
from checksums import compute_sha256, verify_sha256  # noqa: F401
from index_client import download_wheel, fetch_package_metadata, publish_wheel  # noqa: F401


def fetch_wheel(
    package: str,
    version: str,
    dest_dir: str = "/app/data/cache",
    mirror_url: str = "http://127.0.0.1:8081",
) -> Path:
    """Fetch the wheel package for package==version from the upstream mirror.

    Parameters
    ----------
    package : str
        Package name.
    version : str
        Package version string.
    dest_dir : str, default '/app/data/cache'
        Directory where the downloaded wheel is stored.
    mirror_url : str, default 'http://127.0.0.1:8081'
        Upstream mirror base URL.

    Returns
    -------
    Path
        Path to the downloaded wheel file.
    """
    raise NotImplementedError("Implement fetch_wheel")


def verify_checksum(wheel_path: Path | str, expected_sha256: str) -> bool:
    """Verify that the wheel file matches expected_sha256.

    Parameters
    ----------
    wheel_path : Path or str
        Path to the wheel file.
    expected_sha256 : str
        Expected 64-character lowercase hexadecimal SHA-256 digest.

    Returns
    -------
    bool
        True if the file's SHA-256 matches expected_sha256, False otherwise.
    """
    raise NotImplementedError("Implement verify_checksum")


def upload_wheel(
    wheel_path: Path | str,
    index_url: str = "http://127.0.0.1:8082",
) -> bool:
    """Publish the wheel artifact to the internal package index.

    Parameters
    ----------
    wheel_path : Path or str
        Path to the wheel file to upload.
    index_url : str, default 'http://127.0.0.1:8082'
        Destination package index URL.

    Returns
    -------
    bool
        True if the upload was successful, False otherwise.
    """
    raise NotImplementedError("Implement upload_wheel")


def sync_package(
    package: str,
    version: str,
    mirror_url: str = "http://127.0.0.1:8081",
    index_url: str = "http://127.0.0.1:8082",
    cache_dir: str = "/app/data/cache",
) -> bool:
    """Coordinate the full download, verification, and publish sequence.

    Parameters
    ----------
    package : str
        Package name.
    version : str
        Package version string.
    mirror_url : str, default 'http://127.0.0.1:8081'
        Upstream mirror URL.
    index_url : str, default 'http://127.0.0.1:8082'
        Internal index URL.
    cache_dir : str, default '/app/data/cache'
        Local download cache directory.

    Returns
    -------
    bool
        True if synchronization succeeded, False otherwise.
    """
    raise NotImplementedError("Implement sync_package")
