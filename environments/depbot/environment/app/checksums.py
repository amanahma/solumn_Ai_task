"""
checksums.py - Cryptographic hashing utilities for depbot.
(COMPLETE - do not edit.)
"""
from __future__ import annotations
import hashlib
from pathlib import Path


def compute_sha256(path: str | Path) -> str:
    """Return the hex SHA-256 digest of the file at path."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().lower()


def verify_sha256(path: str | Path, expected: str) -> bool:
    """Return True if the file's SHA-256 matches expected hex digest."""
    return compute_sha256(path) == expected.strip().lower()
