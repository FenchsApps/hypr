# Hyprland Rice

Hyprland configuration with three themes, custom scripts, and full component integration.

**Author:** FenchsApps

## Structure

```
hypr/
├── hyprland.conf          # Main Hyprland config
├── hyprpaper.conf         # Wallpaper
├── waybar/                # Bar (config + styles)
├── wofi/                  # App launcher
├── kitty/                 # Terminal
├── dunst/                 # Notifications
├── swaylock/              # Lock screen
├── fastfetch/             # System info
├── neofetch/              # System info (alt)
├── hyfetch.json           # HyFetch (neofetch + flags)
├── scripts/
│   ├── theme-manager.py   # GTK4 theme manager (3 themes)
│   ├── cheatsheet.py      # GTK4 keybinds cheatsheet
│   ├── float-at-cursor.sh # Float window at cursor position
│   ├── cava-waybar.sh     # Audio visualizer for waybar
│   ├── wallpaper.sh       # Wallpaper picker via wofi
│   └── themes.json        # Theme definitions
└── install.sh             # Symlink installer
```

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

The script creates symlinks in `~/.config/` for waybar, wofi, kitty, dunst, swaylock, neofetch, fastfetch, and hyfetch.

## Required Programs

### Core
- [Hyprland](https://hyprland.org) — Wayland compositor
- [Waybar](https://github.com/Alexays/Waybar) — status bar
- [Wofi](https://hg.sr.ht/~scoopta/wofi) — app launcher
- [Kitty](https://sw.kovidgoyal.net/kitty/) — terminal
- [Dunst](https://dunst-project.org) — notifications
- [Swaylock](https://github.com/swaywm/swaylock) — lock screen
- [Hyprpaper](https://github.com/hyprwm/hyprpaper) — wallpaper

### Audio
- [PipeWire](https://pipewire.org) + WirePlumber + pipewire-pulse
- [PavuControl](https://freedesktop.org/software/pulseaudio/pavucontrol/) — volume control
- [Cava](https://github.com/karlstav/cava) — audio visualizer

### Bluetooth & Network
- [Blueman](https://github.com/blueman-project/blueman) — Bluetooth manager
- [NetworkManager](https://networkmanager.dev) + nm-applet

### Utilities
- [grim](https://sr.ht/~emersion/grim/) + [slurp](https://github.com/emersion/slurp) — screenshots
- [wl-clipboard](https://github.com/bugaevc/wl-clipboard) — clipboard
- [jq](https://jqlang.github.io/jq/) — JSON parsing (scripts)
- [brightnessctl](https://github.com/Haikarainen/light) — brightness

### System Info
- [Fastfetch](https://github.com/fastfetch-cli/fastfetch)
- [Neofetch](https://github.com/dylanaraps/neofetch)
- [HyFetch](https://github.com/hykilpikonna/hyfetch)

### Python (for scripts)
- Python 3 + GTK4 (`gi.repository`)
- [Pillow](https://python-pillow.org) — Kitty gradients

### Fonts
- [FiraCode Nerd Font](https://www.nerdfonts.com)

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
