#!/bin/sh

set -e

HYPR_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$(dirname "$HYPR_DIR")"
HOME_DIR="$(dirname "$CONFIG_DIR")"

echo "┌─────────────────────────────────────┐"
echo "│       Hyprland Dotfiles Install     │"
echo "└─────────────────────────────────────┘"
echo ""

# ── Symlink config directories into ~/.config/ ──

echo "Symlinking config directories..."

for dir in waybar wofi swaylock dunst kitty neofetch fastfetch nvim; do
    target="$CONFIG_DIR/$dir"
    if [ -L "$target" ]; then
        rm "$target"
    elif [ -d "$target" ]; then
        echo "  WARNING: $target exists (not a symlink), skipping."
        continue
    fi
    ln -s "$HYPR_DIR/$dir" "$target"
    echo "  $dir -> OK"
done

# ── Symlink single config files into ~/.config/ ──

hyfetch_target="$CONFIG_DIR/hyfetch.json"
if [ -L "$hyfetch_target" ]; then
    rm "$hyfetch_target"
elif [ -f "$hyfetch_target" ]; then
    echo "  WARNING: $hyfetch_target exists (not a symlink), skipping."
fi
if [ ! -e "$hyfetch_target" ]; then
    ln -s "$HYPR_DIR/hyfetch.json" "$hyfetch_target"
    echo "  hyfetch.json -> OK"
fi

# ── Symlink home dotfiles (~/.zshrc, ~/.p10k.zsh) ──

echo ""
echo "Symlinking home dotfiles..."

for dotfile in zshrc p10k.zsh; do
    src="$HYPR_DIR/$dotfile"
    target="$HOME_DIR/.$dotfile"

    if [ ! -f "$src" ]; then
        echo "  SKIP: $dotfile not found in dotfiles"
        continue
    fi

    if [ -L "$target" ]; then
        rm "$target"
    elif [ -f "$target" ]; then
        echo "  Backing up $target -> ${target}.bak"
        mv "$target" "${target}.bak"
    fi
    ln -s "$src" "$target"
    echo "  ~/.$dotfile -> OK"
done

# ── Generate gentoo-icon.png from SVG ──

echo ""
echo "Generating gentoo-icon.png..."

if command -v rsvg-convert >/dev/null 2>&1; then
    rsvg-convert -w 18 -h 18 "$HYPR_DIR/gentoo-white.svg" -o "$HYPR_DIR/gentoo-icon.png"
    echo "  gentoo-icon.png -> OK"
elif command -v magick >/dev/null 2>&1; then
    magick "$HYPR_DIR/gentoo-white.svg" -resize 18x18 "$HYPR_DIR/gentoo-icon.png"
    echo "  gentoo-icon.png -> OK (via ImageMagick)"
elif command -v convert >/dev/null 2>&1; then
    convert "$HYPR_DIR/gentoo-white.svg" -resize 18x18 "$HYPR_DIR/gentoo-icon.png"
    echo "  gentoo-icon.png -> OK (via convert)"
else
    echo "  WARNING: no SVG converter found (install librsvg or imagemagick)"
fi

# ── oh-my-zsh + plugins + powerlevel10k ──

echo ""
echo "Setting up zsh environment..."

if [ ! -d "$HOME_DIR/.oh-my-zsh" ]; then
    echo "  Installing oh-my-zsh..."
    RUNZSH=no CHSH=no sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    # remove generated .zshrc — ours is symlinked
    rm -f "$HOME_DIR/.zshrc"
    ln -s "$HYPR_DIR/zshrc" "$HOME_DIR/.zshrc"
    echo "  oh-my-zsh -> OK"
else
    echo "  oh-my-zsh -> already installed"
fi

ZSH_CUSTOM="${HOME_DIR}/.oh-my-zsh/custom"

if [ ! -d "$ZSH_CUSTOM/themes/powerlevel10k" ]; then
    echo "  Installing powerlevel10k..."
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "$ZSH_CUSTOM/themes/powerlevel10k"
    echo "  powerlevel10k -> OK"
else
    echo "  powerlevel10k -> already installed"
fi

for plugin in zsh-autosuggestions zsh-syntax-highlighting; do
    if [ ! -d "$ZSH_CUSTOM/plugins/$plugin" ]; then
        echo "  Installing $plugin..."
        git clone https://github.com/zsh-users/$plugin "$ZSH_CUSTOM/plugins/$plugin"
        echo "  $plugin -> OK"
    else
        echo "  $plugin -> already installed"
    fi
done

# ── nvim plugins (lazy.nvim bootstrap) ──

echo ""
echo "Setting up neovim plugins..."

if command -v nvim >/dev/null 2>&1; then
    nvim --headless "+Lazy! sync" +qa 2>/dev/null || true
    echo "  nvim plugins -> OK"
else
    echo "  SKIP: nvim not found"
fi

# ── Dependencies check ──

echo ""
echo "Checking dependencies..."

check() {
    if command -v "$1" >/dev/null 2>&1; then
        printf "  %-22s OK\n" "$1"
    else
        printf "  %-22s NOT FOUND\n" "$1"
    fi
}

check hyprland
check waybar
check wofi
check kitty
check dunst
check swaylock
check hyprpaper
check pipewire
check wireplumber
check pavucontrol
check playerctl
check blueman-manager
check nm-applet
check grim
check slurp
check wl-copy
check brightnessctl
check jq
check zsh
check nvim
check fastfetch
check cava

if python3 -c "from PIL import Image" 2>/dev/null; then
    printf "  %-22s OK\n" "python3-pillow"
else
    printf "  %-22s NOT FOUND\n" "python3-pillow"
fi

if python3 -c "import gi; gi.require_version('Gtk','4.0')" 2>/dev/null; then
    printf "  %-22s OK\n" "python3-gtk4"
else
    printf "  %-22s NOT FOUND\n" "python3-gtk4"
fi

echo ""
echo "Done!"
