#!/bin/bash
if ! pgrep -f "api_server.py" >/dev/null 2>&1; then
    python3 /app/api_server.py &
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
