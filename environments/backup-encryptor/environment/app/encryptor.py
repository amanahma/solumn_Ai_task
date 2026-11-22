"""
encryptor.py — Encryption and decryption for the backup service.
"""
from __future__ import annotations
from pathlib import Path
from cryptography.fernet import Fernet
from keystore import escrow_key, ESCROW_PATH  # noqa: F401


def encrypt_directory(src: str, dst: str, key: bytes) -> None:
    """Encrypt the files found under src using Fernet with key.

    The encrypted output is written to dst, reproducing the directory
    structure of src. Each file's plaintext bytes become its
    Fernet-encrypted ciphertext at the corresponding path under dst.

    Parameters
    ----------
    src : str
        Path to the directory containing plaintext files.
    dst : str
        Path to the directory where encrypted files are written.
    key : bytes
        A valid Fernet key (32 url-safe base64-encoded bytes).
    """
    raise NotImplementedError("Implement encrypt_directory")


def decrypt_directory(src: str, dst: str, key: bytes) -> None:
    """Decrypt the files found under src using Fernet with key.

    The decrypted output is written to dst, reproducing the directory
    structure of src.

    Parameters
    ----------
    src : str
        Path to the directory containing Fernet-encrypted files.
    dst : str
        Path to the directory where decrypted files are written.
    key : bytes
        The Fernet key used to encrypt the files.
    """
    raise NotImplementedError("Implement decrypt_directory")
