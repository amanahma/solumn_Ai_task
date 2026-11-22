#!/usr/bin/env sh
set -e

# Run autoresponder daemon or keep alive
echo "[entrypoint] support-autoresponder container ready"

if [ $# -gt 0 ]; then
    exec "$@"
else
    tail -f /dev/null
fi
