#!/bin/sh

HYPR_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$(dirname "$HYPR_DIR")"

for dir in waybar wofi swaylock dunst kitty neofetch fastfetch; do
    target="$CONFIG_DIR/$dir"
    if [ -L "$target" ]; then
        rm "$target"
    elif [ -d "$target" ]; then
        echo "WARNING: $target already exists (not a symlink), skipping. Remove manually."
        continue
    fi
    ln -s "$HYPR_DIR/$dir" "$target"
    echo "$target -> $HYPR_DIR/$dir"
done

# hyfetch.json is a file, not a directory
hyfetch_target="$CONFIG_DIR/hyfetch.json"
if [ -L "$hyfetch_target" ]; then
    rm "$hyfetch_target"
elif [ -f "$hyfetch_target" ]; then
    echo "WARNING: $hyfetch_target already exists (not a symlink), skipping."
fi
if [ ! -e "$hyfetch_target" ]; then
    ln -s "$HYPR_DIR/hyfetch.json" "$hyfetch_target"
    echo "$hyfetch_target -> $HYPR_DIR/hyfetch.json"
fi

echo ""
echo "Checking dependencies for Theme Manager..."
if python3 -c "from PIL import Image" 2>/dev/null; then
    echo "  Pillow — OK"
else
    echo "  Pillow — NOT FOUND (kitty gradients won't work)"
    echo "  Install: pip install Pillow"
fi

echo ""
echo "Done!"
