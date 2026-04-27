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

# Make executables
chmod +x bin/serpent.sh bin/start77 bin/kill77

# Symlink (global command)
sudo ln -sf "$(pwd)/bin/serpent.sh" /usr/local/bin/serpent
sudo ln -sf "$(pwd)/bin/start77" /usr/local/bin/start77
sudo ln -sf "$(pwd)/bin/kill77" /usr/local/bin/kill77

echo "[Serpent] Installed successfully!"
echo "Run: serpent /path/to/logfile"
echo "Or use: start77 /var/log/syslog && kill77"
