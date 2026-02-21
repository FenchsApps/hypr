#!/bin/sh

WALLPAPER_DIRS="$HOME/Pictures $HOME/Downloads"
HYPRPAPER_CONF="$HOME/.config/hypr/hyprpaper.conf"

current_wallpaper() {
    grep '^wallpaper' "$HYPRPAPER_CONF" | sed 's/wallpaper = , //'
}

set_wallpaper() {
    wall="$1"
    old="$(current_wallpaper)"

    hyprctl hyprpaper preload "$wall" 2>/dev/null
    hyprctl hyprpaper wallpaper ", $wall" 2>/dev/null
    [ -n "$old" ] && hyprctl hyprpaper unload "$old" 2>/dev/null

    cat > "$HYPRPAPER_CONF" <<EOF
preload = $wall
wallpaper = , $wall
splash = false
ipc = on
EOF

    notify-send -i "$wall" "Wallpaper updated" "$(basename "$wall")" 2>/dev/null
}

pick_wofi() {
    find $WALLPAPER_DIRS -maxdepth 2 -type f \
        \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \
           -o -iname '*.webp' -o -iname '*.bmp' \) 2>/dev/null \
        | sort \
        | wofi --dmenu --prompt "Pick wallpaper" \
               --width 600 --height 400 --cache-file /dev/null
}

pick_random() {
    dir="${1:-$HOME/Pictures}"
    find "$dir" -maxdepth 2 -type f \
        \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \
           -o -iname '*.webp' -o -iname '*.bmp' \) 2>/dev/null \
        | shuf -n 1
}

case "${1:-}" in
    --random|-r)
        wall="$(pick_random "$2")"
        [ -z "$wall" ] && { echo "No images found"; exit 1; }
        set_wallpaper "$wall"
        ;;
    --set|-s)
        [ -z "$2" ] && { echo "Usage: $0 --set /path/to/wallpaper.jpg"; exit 1; }
        [ ! -f "$2" ] && { echo "File not found: $2"; exit 1; }
        set_wallpaper "$2"
        ;;
    --help|-h)
        cat <<HELP
wallpaper.sh — wallpaper changer for Hyprland + hyprpaper

Usage:
  wallpaper.sh              Open picker menu (wofi)
  wallpaper.sh --random     Random wallpaper from ~/Pictures
  wallpaper.sh -r /path     Random wallpaper from given directory
  wallpaper.sh --set FILE   Set specific file
  wallpaper.sh --help       This help
HELP
        ;;
    *)
        wall="$(pick_wofi)"
        [ -z "$wall" ] && exit 0
        set_wallpaper "$wall"
        ;;
esac
