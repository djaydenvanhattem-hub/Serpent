#!/bin/bash

set -e

echo "=================================="
echo "🐍 Serpent Installer (FULL v7)"
echo "=================================="

REPO_SSH="git@github.com:djaydenvanhattem-hub/serpent.git"
REPO_HTTPS="https://github.com/djaydenvanhattem-hub/serpent.git"

SERPENT_USER="serpent"
INSTALL_DIR="/home/$SERPENT_USER/serpent"

# -----------------------------
# 1. CREATE USER + PASSWORD
# -----------------------------
echo "[1/10] Checking system user..."

if id "$SERPENT_USER" &>/dev/null; then
    echo "✅ User $SERPENT_USER already exists"
else
    echo "➕ Creating user $SERPENT_USER..."

    while true; do
        read -s -p "Enter password for $SERPENT_USER: " PASS1
        echo
        read -s -p "Confirm password: " PASS2
        echo

        if [ "$PASS1" != "$PASS2" ]; then
            echo "❌ Passwords do not match. Try again."
        elif [ -z "$PASS1" ]; then
            echo "❌ Password cannot be empty."
        else
            break
        fi
    done

    sudo useradd -m -s /bin/bash "$SERPENT_USER"
    echo "$SERPENT_USER:$PASS1" | sudo chpasswd

    unset PASS1 PASS2

    echo "✅ User created"
fi

# -----------------------------
# 2. SYSTEM UPDATE
# -----------------------------
echo "[2/10] Updating system..."
sudo apt update && sudo apt upgrade -y

# -----------------------------
# 3. INSTALL DEPENDENCIES
# -----------------------------
echo "[3/10] Installing dependencies..."
sudo apt install -y git python3 python3-pip

# -----------------------------
# 4. SSH CHECK
# -----------------------------
echo "[4/10] Testing SSH access..."

SSH_OK=0
ssh -T git@github.com -o BatchMode=yes 2>&1 | grep -q "successfully authenticated" && SSH_OK=1 || SSH_OK=0

# -----------------------------
# 5. CLEAN INSTALL DIR
# -----------------------------
echo "[5/10] Cleaning old installation..."
sudo rm -rf "$INSTALL_DIR"

# -----------------------------
# 6. CLONE REPO
# -----------------------------
echo "[6/10] Cloning repository..."

if [ "$SSH_OK" -eq 1 ]; then
    echo "✅ Using SSH clone"
    sudo -u "$SERPENT_USER" git clone "$REPO_SSH" "$INSTALL_DIR"
else
    echo "⚠️ SSH failed, using HTTPS fallback"
    sudo -u "$SERPENT_USER" git clone "$REPO_HTTPS" "$INSTALL_DIR"
fi

if [ ! -d "$INSTALL_DIR" ]; then
    echo "❌ Clone failed"
    exit 1
fi

# -----------------------------
# 7. OWNERSHIP FIX
# -----------------------------
echo "[7/10] Fixing ownership..."
sudo chown -R "$SERPENT_USER:$SERPENT_USER" "$INSTALL_DIR"

# -----------------------------
# 8. INSTALL PYTHON DEPS
# -----------------------------
echo "[8/10] Installing Python dependencies..."
sudo pip3 install -r "$INSTALL_DIR/requirements.txt"

# -----------------------------
# 9. PERMISSIONS
# -----------------------------
echo "[9/10] Setting permissions..."
chmod -R 755 "$INSTALL_DIR"
find "$INSTALL_DIR" -type f -exec chmod 644 {} \;
find "$INSTALL_DIR" -type d -exec chmod 755 {} \;
# Ensure bin scripts are executable
chmod 755 "$INSTALL_DIR/bin/serpent.sh"
chmod 755 "$INSTALL_DIR/bin/start77"
chmod 755 "$INSTALL_DIR/bin/kill77"

# -----------------------------
# 10. CLI INSTALL
# -----------------------------
echo "[10/10] Installing CLI..."

sudo ln -sf "$INSTALL_DIR/bin/serpent.sh" /usr/local/bin/serpent
sudo ln -sf "$INSTALL_DIR/bin/start77" /usr/local/bin/start77
sudo ln -sf "$INSTALL_DIR/bin/kill77" /usr/local/bin/kill77

# Add /usr/local/bin to system-wide PATH via profile.d
sudo tee /etc/profile.d/serpent-path.sh > /dev/null <<EOF
export PATH="\$PATH:/usr/local/bin"
EOF
sudo chmod 644 /etc/profile.d/serpent-path.sh

# -----------------------------
# DONE
# -----------------------------
echo ""
echo "=================================="
echo "✅ Serpent installed successfully!"
echo "=================================="
echo ""
echo "User: $SERPENT_USER"
echo "Path: $INSTALL_DIR"
echo ""
echo "Run:"
echo "  serpent test.log"
echo "  serpent test.log --web"
echo "=================================="
