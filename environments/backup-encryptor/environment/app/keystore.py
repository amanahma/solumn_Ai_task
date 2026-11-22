"""
keystore.py — Key escrow utilities for the backup service. (COMPLETE — do not edit.)
"""
from __future__ import annotations
import os
from pathlib import Path

ESCROW_PATH = os.environ.get("ESCROW_PATH", "/app/secure-storage/backup.key")


def escrow_key(key: bytes, path: str = ESCROW_PATH) -> None:
    """Write key bytes to path in secure storage.

    Parameters
    ----------
    key : bytes
        Raw key bytes to persist.
    path : str
        Destination file path. Parent directories are created if absent.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(key)
    print(f"[keystore] key escrowed to {path}", flush=True)


def load_key(path: str = ESCROW_PATH) -> bytes:
    """Read and return key bytes from secure storage.

    Parameters
    ----------
    path : str
        Path from which to load the key.

    Returns
    -------
    bytes
        Raw key bytes.
    """
    return Path(path).read_bytes()
