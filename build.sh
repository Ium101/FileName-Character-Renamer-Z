#!/bin/bash

SCRIPT_NAME="filename-character-remover-z.py"
APP_NAME="Filename Character Remover Z"
DESKTOP_FILE_NAME="filename-character-remover-z.desktop"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/scalable/apps"
DESKTOP_DIR=$(xdg-user-dir DESKTOP 2>/dev/null || echo "$HOME/Desktop")

echo "=========================================="
echo "  Building $APP_NAME for Linux"
echo "=========================================="

if [ ! -f "$SCRIPT_DIR/$SCRIPT_NAME" ]; then
    echo "ERROR: $SCRIPT_NAME not found in $SCRIPT_DIR"
    exit 1
fi

mkdir -p "$APP_DIR" "$DESKTOP_DIR" "$ICON_DIR"

# Install dependencies
echo "[INFO] Installing dependencies..."
python3 -m pip install pillow --break-system-packages -q 2>/dev/null || \
    python3 -m pip install pillow -q 2>/dev/null || true

# Sanity check: tkinter must come from the system Python, not pip
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "[WARN] tkinter not found for python3. Install it via your distro"
    echo "       package manager (e.g. 'sudo pacman -S tk' or 'sudo apt install python3-tk')."
fi

# Clean old artifacts
echo "[INFO] Cleaning old artifacts..."
rm -rf "$SCRIPT_DIR/__pycache__/"

# ---------------------------------------------------------------------------
# Install SVG icon — exported from the same base64 icon embedded in the .py
# source (single source of truth, also used for the live window icon).
# Transparent background, teal document + Z badge, no black anywhere.
# ---------------------------------------------------------------------------
echo "[INFO] Installing icon..."
ICON_PATH="$ICON_DIR/filename-character-remover-z.svg"
python3 "$SCRIPT_DIR/$SCRIPT_NAME" --generate-icon --svg="$ICON_PATH"
if [ ! -f "$ICON_PATH" ]; then
    echo "[WARN] Icon generation failed, continuing without icon."
fi

# Also put a copy in the flat icons dir (for DEs that look there)
ICON_DIR_FLAT="$HOME/.local/share/icons"
cp "$ICON_PATH" "$ICON_DIR_FLAT/filename-character-remover-z.svg"

# No PyInstaller executable is built anymore on Linux — shortcuts run the
# .py script directly via python3, so just make sure it's executable.
chmod +x "$SCRIPT_DIR/$SCRIPT_NAME"

# ---------------------------------------------------------------------------
# Write the .desktop entry (system menu / Start Menu equivalent)
# ---------------------------------------------------------------------------
echo "[INFO] Registering in system menu..."
DESKTOP_ENTRY_CONTENT="[Desktop Entry]
Name=$APP_NAME
Comment=Remove custom characters from filenames / Remover caracteres de nomes de arquivo
Exec=python3 \"$SCRIPT_DIR/$SCRIPT_NAME\"
Icon=filename-character-remover-z
Terminal=false
Type=Application
Categories=Utility;FileTools;FileManager;
StartupNotify=true
"

# Write to applications dir (Start Menu)
printf '%s' "$DESKTOP_ENTRY_CONTENT" > "$APP_DIR/$DESKTOP_FILE_NAME"
chmod 644 "$APP_DIR/$DESKTOP_FILE_NAME"

# ---------------------------------------------------------------------------
# Write the Desktop shortcut
# ---------------------------------------------------------------------------
echo "[INFO] Creating Desktop shortcut..."
printf '%s' "$DESKTOP_ENTRY_CONTENT" > "$DESKTOP_DIR/$DESKTOP_FILE_NAME"
chmod 755 "$DESKTOP_DIR/$DESKTOP_FILE_NAME"

# Mark as trusted (suppresses GNOME/KDE "Untrusted launcher" prompt)
if command -v gio &>/dev/null; then
    gio set "$DESKTOP_DIR/$DESKTOP_FILE_NAME" metadata::trusted true 2>/dev/null
fi
# KDE/Plasma: mark executable bit already covers trust — but also set xattr if attr is present
if command -v attr &>/dev/null; then
    attr -s "user.baloo.rating" -V 0 "$DESKTOP_DIR/$DESKTOP_FILE_NAME" 2>/dev/null || true
fi

# ---------------------------------------------------------------------------
# Refresh desktop databases / caches
# ---------------------------------------------------------------------------
echo "[INFO] Refreshing menu and icon caches..."

# XDG application database
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database "$APP_DIR" 2>/dev/null
fi

# GTK icon cache
if command -v gtk-update-icon-cache &>/dev/null; then
    gtk-update-icon-cache -f -t "$HOME/.local/share/icons" 2>/dev/null || true
fi

# KDE / Plasma menu cache
if command -v kbuildsycoca6 &>/dev/null; then
    kbuildsycoca6 --noincremental 2>/dev/null
elif command -v kbuildsycoca5 &>/dev/null; then
    kbuildsycoca5 --noincremental 2>/dev/null
fi

# Notify the file manager / shell that desktop has changed
if command -v xdg-open &>/dev/null && command -v xdotool &>/dev/null; then
    true  # no-op; just ensuring gio set above was enough
fi

# ---------------------------------------------------------------------------
# Clean up stray artifacts
# ---------------------------------------------------------------------------
echo "[INFO] Cleaning up..."
rm -rf "$SCRIPT_DIR/__pycache__/"

echo ""
echo "=========================================="
echo "  Done!"
echo "  Script     : $SCRIPT_DIR/$SCRIPT_NAME"
echo "  Icon       : $ICON_PATH"
echo "  Menu entry : $APP_DIR/$DESKTOP_FILE_NAME"
echo "  Desktop    : $DESKTOP_DIR/$DESKTOP_FILE_NAME"
echo ""
echo "  Features in the app:"
echo "   - Dark/Light theme toggle (🌙 / ☀️ button, top-right)"
echo "   - Remembers last selected folder between sessions"
echo "   - Native KDE folder picker (kdialog) when available"
echo "   - Falls back to tkinter dialog on other DEs"
echo ""
echo "  If the desktop icon shows 'Untrusted':"
echo "    Right-click it -> Properties -> Permissions -> Allow executing"
echo "    Or: chmod +x \"$DESKTOP_DIR/$DESKTOP_FILE_NAME\""
echo "=========================================="
