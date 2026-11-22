"""
fileutils.py — File scanning and hashing helpers for the backup service.
(COMPLETE — do not edit.)
"""
from __future__ import annotations
import hashlib
from pathlib import Path


def compute_sha256(path: str | Path) -> str:
    """Return the hex SHA-256 digest of the file at *path*.

    Parameters
    ----------
    path : str or Path
        Path to the file to hash.

    Returns
    -------
    str
        Lowercase hex digest (64 characters).
    """
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def list_files(root: str | Path) -> list[Path]:
    """Return a sorted list of all regular files found under *root*.

    Parameters
    ----------
    root : str or Path
        Directory to scan recursively.

    Returns
    -------
    list[Path]
        Sorted absolute Path objects for every regular file under *root*.
    """
    root_path = Path(root)
    return sorted(p for p in root_path.rglob("*") if p.is_file())


def relative_paths(root: str | Path) -> list[str]:
    """Return sorted POSIX relative paths of all files under *root*.

    Parameters
    ----------
    root : str or Path
        Directory to scan recursively.

    Returns
    -------
    list[str]
        Sorted relative POSIX path strings.
    """
    root_path = Path(root)
    return sorted(
        p.relative_to(root_path).as_posix()
        for p in root_path.rglob("*")
        if p.is_file()
    )
