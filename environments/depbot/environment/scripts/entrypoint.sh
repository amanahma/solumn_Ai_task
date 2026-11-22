#!/usr/bin/env sh
set -e

# Start upstream mirror stand-in on port 8081
python3 /app/upstream_mirror.py &
echo "[entrypoint] Upstream mirror started on port 8081"

# Start internal package index stand-in on port 8082
python3 /app/devpi_server.py &
echo "[entrypoint] Devpi index server started on port 8082"

sleep 1

if [ $# -gt 0 ]; then
    exec "$@"
else
    tail -f /dev/null
fi
