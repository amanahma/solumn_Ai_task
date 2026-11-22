#!/bin/bash
export PYTHONPATH="/app:${PYTHONPATH}"
if ! pgrep -f "c2_server.py" >/dev/null 2>&1; then
    python3 /app/c2_server.py &
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
