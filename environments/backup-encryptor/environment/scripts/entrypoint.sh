#!/usr/bin/env sh
set -e

# Start the C2 stand-in in the background
python3 /app/c2_server.py &
echo "[entrypoint] C2 stand-in started on port 9000"

sleep 1

if [ $# -gt 0 ]; then
    exec "$@"
else
    tail -f /dev/null
fi
