#!/bin/bash
export PYTHONPATH="/app:${PYTHONPATH}"
ip addr add 203.0.113.42/32 dev lo 2>/dev/null || true
if ! pgrep -f "standin_server.py" >/dev/null 2>&1; then
    python3 /app/standin_server.py &
    sleep 1
fi
mkdir -p /logs/verifier
python3 /tests/grader.py
if [ -f /app/reward.txt ]; then
  cp /app/reward.txt /logs/verifier/reward.txt
fi
if [ -f /app/result.json ]; then
  cp /app/result.json /logs/verifier/result.json
fi
