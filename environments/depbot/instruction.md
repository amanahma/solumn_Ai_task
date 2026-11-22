# Ticket DB-340: Implement wheel synchronization in depbot

## Background

The platform engineering team uses `depbot` to synchronize approved dependency
wheels from our upstream mirror into our internal private package index.

The synchronization pipeline is orchestrated by `depbot_runner.py`, which is
already implemented. It relies on four functions in `updater.py` that need to be
completed:

- `fetch_wheel(package, version, dest_dir)` - download wheel from the upstream mirror
- `verify_checksum(wheel_path, expected_sha256)` - verify wheel SHA-256 integrity
- `upload_wheel(wheel_path, index_url)` - publish wheel to the internal package index
- `sync_package(package, version)` - coordinate the full download, verification, and upload sequence

Support modules for SHA-256 computation (`checksums.py`), package index client
interactions (`index_client.py`), and upstream mirror queries (`upstream_mirror.py`)
are provided in the repository.

## Functions to implement

### `fetch_wheel(package: str, version: str, dest_dir: str) -> Path`

Retrieve the wheel artifact for `package==version` from the upstream mirror and
save it into `dest_dir`.

| Parameter  | Type  | Description |
|------------|-------|-------------|
| `package`  | `str` | Package name. |
| `version`  | `str` | Package version string. |
| `dest_dir` | `str` | Directory path where the downloaded wheel is written. |

Returns the `Path` to the downloaded `.whl` file on disk.

### `verify_checksum(wheel_path: Path | str, expected_sha256: str) -> bool`

Verify the SHA-256 digest of the specified wheel against `expected_sha256`.

| Parameter         | Type           | Description |
|-------------------|----------------|-------------|
| `wheel_path`      | `Path \| str`  | Path to the wheel file. |
| `expected_sha256` | `str`          | Expected 64-character lowercase hexadecimal SHA-256 digest. |

Returns `True` if the file's SHA-256 matches `expected_sha256`, `False` otherwise.

### `upload_wheel(wheel_path: Path | str, index_url: str) -> bool`

Publish the wheel artifact at `wheel_path` to the internal package index at `index_url`.

| Parameter    | Type          | Description |
|--------------|---------------|-------------|
| `wheel_path` | `Path \| str` | Path to the wheel file to upload. |
| `index_url`  | `str`         | Destination internal index URL. |

Returns `True` if the upload succeeded with HTTP 200/201, `False` otherwise.

### `sync_package(package: str, version: str) -> bool`

Execute the full synchronization sequence for `package==version`: query the
upstream mirror for package metadata, download the wheel into the download cache,
verify its checksum, and publish the wheel to the internal index.

| Parameter | Type  | Description |
|-----------|-------|-------------|
| `package` | `str` | Package name. |
| `version` | `str` | Package version string. |

Returns `True` if synchronization completed successfully, `False` otherwise.

## Acceptance criteria

1. `python depbot_runner.py` exits with code 0.
2. The package wheel is published to the internal package index repository.
3. The published wheel is a valid `.whl` zip archive containing standard metadata
   matching the requested package and version.
