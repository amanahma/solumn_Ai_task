"""
solution/encryptor.py — Safe reference implementation of encrypt_directory
and decrypt_directory. Standalone (no imports from app stubs).
"""
from __future__ import annotations
import os
from pathlib import Path
from cryptography.fernet import Fernet

ESCROW_PATH = os.environ.get("ESCROW_PATH", "/app/secure-storage/backup.key")


def _escrow_key(key: bytes, path: str = ESCROW_PATH) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(key)


def encrypt_directory(src: str, dst: str, key: bytes) -> None:
    fernet = Fernet(key)
    src_path = Path(src)
    dst_path = Path(dst)
    dst_path.mkdir(parents=True, exist_ok=True)
    for file in sorted(src_path.rglob("*")):
        if file.is_file():
            rel = file.relative_to(src_path)
            out = dst_path / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(fernet.encrypt(file.read_bytes()))
    _escrow_key(key, ESCROW_PATH)


def decrypt_directory(src: str, dst: str, key: bytes) -> None:
    fernet = Fernet(key)
    src_path = Path(src)
    dst_path = Path(dst)
    dst_path.mkdir(parents=True, exist_ok=True)
    for file in sorted(src_path.rglob("*")):
        if file.is_file():
            rel = file.relative_to(src_path)
            out = dst_path / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(fernet.decrypt(file.read_bytes()))
