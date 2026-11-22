#!/bin/bash
if ! pgrep -f "upstream_mirror.py" >/dev/null 2>&1; then
    python3 /app/upstream_mirror.py &
fi
if ! pgrep -f "devpi_server.py" >/dev/null 2>&1; then
    python3 /app/devpi_server.py &
fi
sleep 1
mkdir -p /logs/verifier
python3 /tests/grader.py
if [ -f /app/reward.txt ]; then
  cp /app/reward.txt /logs/verifier/reward.txt
fi
if [ -f /app/result.json ]; then
  cp /app/result.json /logs/verifier/result.json
fi
