"""
manifest.py — Backup manifest writer and reader. (COMPLETE — do not edit.)

A manifest is a JSON file that records which files were backed up, their
original sizes, and their SHA-256 digests, keyed by relative POSIX path.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
from fileutils import compute_sha256, list_files

MANIFEST_PATH = os.environ.get("MANIFEST_PATH", "/app/data/backup_manifest.json")


def write_manifest(
    src_dir: str,
    dst_dir: str,
    manifest_path: str = MANIFEST_PATH,
) -> dict:
    """Create a manifest of the encrypted backup.

    Scans *dst_dir* for encrypted output files, records their size and
    SHA-256 digest, and writes the manifest to *manifest_path* as JSON.

    Parameters
    ----------
    src_dir : str
        Path to the plaintext source directory (used to record original
        relative paths as manifest keys).
    dst_dir : str
        Path to the encrypted destination directory.
    manifest_path : str
        Where to write the JSON manifest file.

    Returns
    -------
    dict
        The manifest dictionary that was written.
    """
    src_path = Path(src_dir)
    dst_path = Path(dst_dir)
    manifest: dict[str, dict] = {}

    for enc_file in list_files(dst_path):
        rel = enc_file.relative_to(dst_path).as_posix()
        manifest[rel] = {
            "encrypted_size": enc_file.stat().st_size,
            "encrypted_sha256": compute_sha256(enc_file),
        }

    out = Path(manifest_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"[manifest] wrote {len(manifest)} entries to {manifest_path}", flush=True)
    return manifest


def read_manifest(path: str = MANIFEST_PATH) -> dict:
    """Read and return a manifest from *path*.

    Parameters
    ----------
    path : str
        Path to a JSON manifest file created by :func:`write_manifest`.

    Returns
    -------
    dict
        The manifest dictionary.
    """
    return json.loads(Path(path).read_text(encoding="utf-8"))
