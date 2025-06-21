#!/bin/bash

# Create Desktop Shortcut for PyNord
# This script creates a .desktop file for easy launching

set -e

# Get the current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="PyNord"
DESKTOP_FILE="$HOME/.local/share/applications/pynord.desktop"

echo "Creating desktop shortcut for PyNord..."

# Create applications directory if it doesn't exist
mkdir -p "$HOME/.local/share/applications"

# Create the .desktop file
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=PyNord
Comment=NordVPN Management Application
Exec=$SCRIPT_DIR/pynord_env/bin/python $SCRIPT_DIR/main.py
Icon=network-vpn
Terminal=false
Categories=Network;Security;
Keywords=VPN;NordVPN;Network;Security;
EOF

# Make the .desktop file executable
chmod +x "$DESKTOP_FILE"

echo "Desktop shortcut created at: $DESKTOP_FILE"
echo "You can now find PyNord in your application menu!"
echo
echo "Note: If you don't see the icon, try logging out and back in,"
echo "or run: update-desktop-database ~/.local/share/applications" 