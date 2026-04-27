#!/bin/bash

echo "[Serpent] Installing..."

# Check python
if ! command -v python3 &> /dev/null
then
    echo "Python3 is required!"
    exit
fi

# Install pip deps
pip3 install -r requirements.txt

# Make executable
chmod +x serpent.sh

# Symlink (global command)
sudo In -sf $(pwd)/serpent.sh /usr/local/bin/serpent

echo "[Serpent] Installed succesfully!"
echo "Run: serpent /path/to/logfile"
