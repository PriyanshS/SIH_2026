#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# install_launcher.sh  —  Install BEL FleetLink Launcher as a desktop app
# ─────────────────────────────────────────────────────────────────────────────
# Usage:  bash /home/piyansh46/Code/SIH_2026/launcher/install_launcher.sh
# ─────────────────────────────────────────────────────────────────────────────

set -e

LAUNCHER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_FILE="$LAUNCHER_DIR/fleetlink-launcher.desktop"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
APPS_DIR="$HOME/.local/share/applications"
BIN_LINK="$HOME/.local/bin/fleetlink"

# 1. Fix Exec path in .desktop to use the real absolute path
sed -i "s|Exec=.*|Exec=python3 $LAUNCHER_DIR/launch_app.py|g" "$DESKTOP_FILE"

# 2. Ensure directories exist
mkdir -p "$APPS_DIR" "$ICON_DIR" "$HOME/.local/bin"

# 3. Copy .desktop file
cp "$DESKTOP_FILE" "$APPS_DIR/fleetlink-launcher.desktop"
chmod 644 "$APPS_DIR/fleetlink-launcher.desktop"

# 4. Validate .desktop (if validation tool available)
if command -v desktop-file-validate &>/dev/null; then
    desktop-file-validate "$APPS_DIR/fleetlink-launcher.desktop" \
        && echo "✓ .desktop file is valid" || true
fi

# 5. Update desktop database
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database "$APPS_DIR" 2>/dev/null || true
fi

# 6. Create CLI symlink for quick access from terminal
chmod +x "$LAUNCHER_DIR/launch_app.py"
ln -sf "$LAUNCHER_DIR/launch_app.py" "$BIN_LINK"

echo ""
echo "════════════════════════════════════════════════════"
echo "  ✅  FleetLink Launcher installed!"
echo ""
echo "  • App menu:  search 'FleetLink' in your launcher"
echo "  • Terminal:  fleetlink"
echo "  • Direct:    python3 $LAUNCHER_DIR/launch_app.py"
echo "════════════════════════════════════════════════════"
