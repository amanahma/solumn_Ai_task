"""
backup_runner.py — Entry point for the nightly backup pipeline.
(COMPLETE — do not edit.)

Loads config, generates a fresh Fernet key, calls encrypt_directory,
writes the backup manifest, and exits 0 on success.
"""
from __future__ import annotations
import os
import sys
import tomllib
from pathlib import Path
from cryptography.fernet import Fernet

from encryptor import encrypt_directory
from manifest import write_manifest

CONFIG_PATH = Path(os.environ.get("CONFIG_PATH", "/app/config.toml"))
if not CONFIG_PATH.exists():
    CONFIG_PATH = Path(__file__).parent / "config.toml"


def load_config() -> dict:
    raw = CONFIG_PATH.read_bytes().lstrip(b"\xef\xbb\xbf")
    return tomllib.loads(raw.decode("utf-8"))


def main() -> int:
    cfg = load_config()
    src = os.environ.get("SRC_DIR", cfg["backup"]["src_dir"])
    dst = os.environ.get("DST_DIR", cfg["backup"]["dst_dir"])

    # Generate a fresh Fernet key for this backup run.
    key = Fernet.generate_key()

    print(f"[runner] starting backup: {src} -> {dst}", flush=True)
    encrypt_directory(src, dst, key)
    print("[runner] encryption complete", flush=True)

    manifest_path = os.environ.get("MANIFEST_PATH", "/app/data/backup_manifest.json")
    write_manifest(src, dst, manifest_path=manifest_path)
    print("[runner] manifest written", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
