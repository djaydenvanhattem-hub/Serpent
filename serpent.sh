#!/bin/bash

LOG_FILE=$1
MODE=$2

if [ -z "$LOG_FILE" ]; then
  echo "Usage: serpent /path/to/logfile [--web]"
  exit 1
fi

if [ "$MODE" == "--web" ]; then
  python3 web.py "$LOG_FILE"
fi
