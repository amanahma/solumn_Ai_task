#!/usr/bin/env sh
set -e

# Alias 203.0.113.42 to loopback so outbound probes to it are caught locally
ip addr add 203.0.113.42/32 dev lo 2>/dev/null || true

# Start stand-in server in background
python3 /app/standin_server.py &
echo "[entrypoint] Stand-in server started"

sleep 1

if [ $# -gt 0 ]; then
    exec "$@"
else
    tail -f /dev/null
fi
