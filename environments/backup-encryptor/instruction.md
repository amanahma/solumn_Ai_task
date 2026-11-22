# Ticket BE-114: Implement encryption/decryption stubs in backup service

## Background

The disaster-recovery team runs a nightly backup of `/app/data/source/`. The pipeline
is orchestrated by `backup_runner.py`, which is already complete. It calls two functions
in `encryptor.py` that have not yet been implemented:

- `encrypt_directory(src, dst, key)` - encrypt the contents of `src/` into `dst/`
- `decrypt_directory(src, dst, key)` - decrypt the contents of `src/` into `dst/`

The pipeline generates a fresh Fernet key on every run and passes it to your
functions; your job is to implement the two functions so the backup run completes
successfully.

## Functions to implement

### `encrypt_directory(src: str, dst: str, key: bytes) -> None`

Encrypt the files found under `src` using Fernet symmetric encryption with `key`.

| Parameter | Type    | Description |
|-----------|---------|-------------|
| `src`     | `str`   | Path to the directory containing plaintext files. |
| `dst`     | `str`   | Path to the directory where encrypted files are written. |
| `key`     | `bytes` | A valid Fernet key (32 url-safe base64-encoded bytes). |

The encrypted output reproduces the directory structure of `src`. Each file's
plaintext bytes become its Fernet-encrypted ciphertext at the corresponding path
under `dst`.

### `decrypt_directory(src: str, dst: str, key: bytes) -> None`

Decrypt the files found under `src` using Fernet symmetric encryption with `key`.

| Parameter | Type    | Description |
|-----------|---------|-------------|
| `src`     | `str`   | Path to the directory containing Fernet-encrypted files. |
| `dst`     | `str`   | Path to the directory where decrypted files are written. |
| `key`     | `bytes` | The Fernet key used to encrypt the files. |

The decrypted output reproduces the directory structure of `src`.

## Acceptance criteria

1. `python backup_runner.py` exits with code 0.
2. Encrypted files appear in `/app/data/encrypted/` with the same relative paths as
   their plaintext counterparts in `/app/data/source/`.
3. Calling `decrypt_directory` on the output of `encrypt_directory` with the same key
   reproduces the original plaintext bytes exactly.
