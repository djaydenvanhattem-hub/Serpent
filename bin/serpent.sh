#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
SRC_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)/src"

if [ "$1" == "--web" ]; then
  FILE="$2"
  MODE="--web"
else
  FILE="$1"
  MODE="$2"
fi

if [ -z "$FILE" ]; then
  echo "Usage: serpent <logfile> [--web]"
  echo "       serpent --web <logfile>"
  exit 1
fi

if [ "$MODE" == "--web" ]; then
  PYTHONPATH="$SRC_ROOT" python3 -m serpent.web "$FILE"
else
  PYTHONPATH="$SRC_ROOT" python3 -m serpent.serpent "$FILE"
fi
