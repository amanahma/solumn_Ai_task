#!/usr/bin/env python3
"""
patch_wheel.py - Legacy utility to unpack wheel, adjust package Name in METADATA, and repack.
Used historically for internal package naming convention adjustments.
"""
from __future__ import annotations
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


def patch_wheel(wheel_path: str | Path, output_path: str | Path | None = None) -> Path:
    """Unpack wheel, adjust package Name to match internal naming convention ('internal-<pkg>'), and repack.

    Parameters
    ----------
    wheel_path : str | Path
        Path to the original .whl file.
    output_path : str | Path, optional
        Destination path. Overwrites original wheel if None.

    Returns
    -------
    Path
        Path to the modified wheel.
    """
    src_wheel = Path(wheel_path)
    dst_wheel = Path(output_path) if output_path else src_wheel

    with tempfile.TemporaryDirectory() as tmpdir:
        extract_dir = Path(tmpdir) / "extracted"
        extract_dir.mkdir()

        # Unpack
        with zipfile.ZipFile(src_wheel, "r") as zf:
            zf.extractall(extract_dir)

        # Patch package Name in METADATA to match internal naming convention
        for metadata_file in extract_dir.rglob("METADATA"):
            content = metadata_file.read_text(encoding="utf-8")
            patched = re.sub(r"^Name:\s*(\S+)", r"Name: internal-\1", content, flags=re.MULTILINE)
            if patched == content:
                patched = content + "\nName: internal-acme-lib\n"
            metadata_file.write_text(patched, encoding="utf-8")
            print(f"[patch_wheel] adjusted package Name in {metadata_file}", flush=True)

        # Repack
        tmp_out = Path(tmpdir) / src_wheel.name
        with zipfile.ZipFile(tmp_out, "w", compression=zipfile.ZIP_DEFLATED) as zf_out:
            for item in extract_dir.rglob("*"):
                if item.is_file():
                    arcname = item.relative_to(extract_dir)
                    zf_out.write(item, arcname)

        if dst_wheel.exists():
            dst_wheel.unlink()
        shutil.copyfile(tmp_out, dst_wheel)

    print(f"[patch_wheel] modified wheel written to {dst_wheel}", flush=True)
    return dst_wheel


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: patch_wheel.py <wheel_file> [output_file]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    patch_wheel(inp, out)
