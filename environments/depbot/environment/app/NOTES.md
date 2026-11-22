# Developer Notes - Internal Build Packaging

Author: dev-infra-lead
Date: 2023-11-10

## Internal Namespace & Naming Convention
Our internal deployment clusters and private package indexes expect packages
to adhere to the internal naming convention (`internal-<pkg>`).

For third-party wheels like `acme-lib`, upstream builds publish without the
internal prefix. We previously maintained `scripts/patch_wheel.py` to adjust the
`Name` field in the wheel's `METADATA` before publishing to our private index.

See `scripts/patch_wheel.py` for the unpack/patch/repack workflow if internal
consumers report missing `internal-*` package references (see also logs/last_sync.log).
