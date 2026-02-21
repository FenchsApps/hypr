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

    notify-send -i "$wall" "Обои обновлены" "$(basename "$wall")" 2>/dev/null
}

pick_wofi() {
    find $WALLPAPER_DIRS -maxdepth 2 -type f \
        \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \
           -o -iname '*.webp' -o -iname '*.bmp' \) 2>/dev/null \
        | sort \
        | wofi --dmenu --prompt "Выбери обои" \
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
        [ -z "$wall" ] && { echo "Изображения не найдены"; exit 1; }
        set_wallpaper "$wall"
        ;;
    --set|-s)
        [ -z "$2" ] && { echo "Использование: $0 --set /путь/к/обоям.jpg"; exit 1; }
        [ ! -f "$2" ] && { echo "Файл не найден: $2"; exit 1; }
        set_wallpaper "$2"
        ;;
    --help|-h)
        cat <<HELP
wallpaper.sh — смена обоев для Hyprland + hyprpaper

Использование:
  wallpaper.sh              Открыть меню выбора (wofi)
  wallpaper.sh --random     Случайные обои из ~/Pictures
  wallpaper.sh -r /путь     Случайные обои из указанной папки
  wallpaper.sh --set ФАЙЛ   Установить конкретный файл
  wallpaper.sh --help       Эта справка
HELP
        ;;
    *)
        wall="$(pick_wofi)"
        [ -z "$wall" ] && exit 0
        set_wallpaper "$wall"
        ;;
esac
