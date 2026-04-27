#!/bin/bash

FILE=$1
MODE=$2

if [ -z "$FILE" ]; then
  echo "Usage: serpent <logfile> [--web]"
  exit 1
fi

if [ "$MODE" == "--web" ]; then
  python3 web.py "$FILE"
else
  python3 serpent.py "$FILE"
fi
