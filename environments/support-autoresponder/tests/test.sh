#!/bin/bash
set -e
mkdir -p /logs/verifier
python3 /tests/grader.py
if [ -f /app/reward.txt ]; then
  cp /app/reward.txt /logs/verifier/reward.txt
fi
if [ -f /app/result.json ]; then
  cp /app/result.json /logs/verifier/result.json
fi
