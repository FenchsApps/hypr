# Hyprland Rice

Hyprland configuration with custom themes, waybar media player, neovim setup, and oh-my-zsh integration.

**Author:** FenchsApps

## Structure

```
hypr/
├── hyprland.conf          # Main Hyprland config
├── hyprpaper.conf         # Wallpaper
├── waybar/                # Bar (config + styles)
├── wofi/                  # App launcher
├── kitty/                 # Terminal (+ gradient background)
├── dunst/                 # Notifications
├── swaylock/              # Lock screen
├── nvim/                  # Neovim config (lazy.nvim + LSP)
├── fastfetch/             # System info
├── neofetch/              # System info (alt)
├── hyfetch.json           # HyFetch (neofetch + flags)
├── zshrc                  # Zsh config (symlinked to ~/.zshrc)
├── p10k.zsh               # Powerlevel10k theme (symlinked to ~/.p10k.zsh)
├── gentoo-white.svg       # Gentoo icon (white, source)
├── gentoo-icon.png        # Gentoo icon (generated at install)
├── scripts/
│   ├── theme-manager.py   # GTK4 theme manager (3 themes)
│   ├── cheatsheet.py      # GTK4 keybinds cheatsheet
│   ├── float-at-cursor.sh # Float window at cursor position
│   ├── cava-waybar.sh     # Audio visualizer for waybar
│   ├── terminal-name.sh   # Current terminal detector for waybar
│   ├── wallpaper.sh       # Wallpaper picker via wofi
│   └── themes.json        # Theme definitions
└── install.sh             # Full installer (symlinks + deps)
```

## Waybar

Rounded pill-style sections with transparent black background. Gentoo icon button on the left, media player with controls in the center, system tray with app icons on the right.

## Themes

| Theme | Accent |
|-------|--------|
| Life is Green | `#39ff14` `#00e676` |
| Truth is Red | `#ff1744` `#ff5252` |
| I am Purple | `#b388ff` `#7c4dff` |

Switch themes: `SUPER + SHIFT + T`

## Install

```bash
git clone <repo> ~/.config/hypr
cd ~/.config/hypr
chmod +x install.sh
./install.sh
```

The script will:
- Create symlinks in `~/.config/` for waybar, wofi, kitty, dunst, swaylock, neofetch, fastfetch, nvim
- Symlink `zshrc` → `~/.zshrc` and `p10k.zsh` → `~/.p10k.zsh`
- Generate `gentoo-icon.png` from SVG
- Install oh-my-zsh, powerlevel10k, zsh-autosuggestions, zsh-syntax-highlighting
- Bootstrap neovim plugins via lazy.nvim
- Check all dependencies

## Required Packages

### Core

| Package | Description |
|---------|-------------|
| [hyprland](https://hyprland.org) | Wayland compositor |
| [waybar](https://github.com/Alexays/Waybar) | Status bar |
| [wofi](https://hg.sr.ht/~scoopta/wofi) | App launcher |
| [kitty](https://sw.kovidgoyal.net/kitty/) | Terminal emulator |
| [dunst](https://dunst-project.org) | Notification daemon |
| [swaylock](https://github.com/swaywm/swaylock) | Lock screen |
| [hyprpaper](https://github.com/hyprwm/hyprpaper) | Wallpaper manager |

### Audio

| Package | Description |
|---------|-------------|
| [pipewire](https://pipewire.org) | Audio server |
| wireplumber | PipeWire session manager |
| pipewire-pulse | PulseAudio compatibility |
| [pavucontrol](https://freedesktop.org/software/pulseaudio/pavucontrol/) | Volume control GUI |
| [playerctl](https://github.com/altdesktop/playerctl) | Media player control (waybar player) |
| [cava](https://github.com/karlstav/cava) | Audio visualizer |

### Network & Bluetooth

| Package | Description |
|---------|-------------|
| [networkmanager](https://networkmanager.dev) | Network management |
| nm-applet | NetworkManager tray applet |
| [blueman](https://github.com/blueman-project/blueman) | Bluetooth manager |

### Shell & Editor

| Package | Description |
|---------|-------------|
| [zsh](https://www.zsh.org) | Shell |
| [oh-my-zsh](https://ohmyz.sh) | Zsh framework (installed by install.sh) |
| [powerlevel10k](https://github.com/romkatv/powerlevel10k) | Zsh theme (installed by install.sh) |
| [neovim](https://neovim.io) | Text editor |

### Utilities

| Package | Description |
|---------|-------------|
| [grim](https://sr.ht/~emersion/grim/) | Screenshot tool |
| [slurp](https://github.com/emersion/slurp) | Region selector |
| [wl-clipboard](https://github.com/bugaevc/wl-clipboard) | Clipboard (wl-copy) |
| [brightnessctl](https://github.com/Haikarainen/light) | Brightness control |
| [jq](https://jqlang.github.io/jq/) | JSON processor (scripts) |
| [librsvg](https://wiki.gnome.org/Projects/LibRsvg) | SVG converter (rsvg-convert, for icon generation) |

### System Info

| Package | Description |
|---------|-------------|
| [fastfetch](https://github.com/fastfetch-cli/fastfetch) | System info |
| [neofetch](https://github.com/dylanaraps/neofetch) | System info (alt) |
| [hyfetch](https://github.com/hykilpikonna/hyfetch) | Neofetch + pride flags |

### Python

| Package | Description |
|---------|-------------|
| python3 | Runtime (for GTK scripts) |
| python3-gtk4 | GTK4 bindings (`gi.repository`) |
| [pillow](https://python-pillow.org) | Image processing (kitty gradients) |

### Fonts

| Package | Description |
|---------|-------------|
| [FiraCode Nerd Font](https://www.nerdfonts.com) | Main UI/terminal font |

## Keybinds

| Combo | Action |
|-------|--------|
| `SUPER + Return` | Kitty |
| `SUPER + Q` | Google Chrome |
| `SUPER + D` | Wofi (launcher) |
| `SUPER + E` | Nautilus |
| `SUPER + X` | Close window |
| `SUPER + F` | Maximize |
| `SUPER + V` | Float |
| `SUPER + SHIFT + SPACE` | Float at cursor |
| `SUPER + SPACE` | Layout EN/RU |
| `SUPER + L` | Lock screen |
| `SUPER + W` | Wallpaper |
| `SUPER + SHIFT + T` | Theme manager |
| `SUPER + SHIFT + H` | Cheatsheet |
| `SUPER + SHIFT + A` | PavuControl |
| `SUPER + SHIFT + B` | Blueman |
| `Print` | Screenshot |
