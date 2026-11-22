#!/usr/bin/env sh
set -e
python3 /app/api_server.py &
API_PID=$!
echo "API stand-in started (pid $API_PID)"
sleep 1
if [ $# -gt 0 ]; then
    exec "$@"
else
    tail -f /dev/null
fi
