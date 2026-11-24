#!/bin/bash
# ps GIẢ LẬP cho thử v4/chay.sh: in "PID ARGS" từ $FAKE/ps.txt (nếu có).
echo "  PID COMMAND"; [ -f "$FAKE/ps.txt" ] && cat "$FAKE/ps.txt"; exit 0
