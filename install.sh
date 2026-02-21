#!/bin/sh

HYPR_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$(dirname "$HYPR_DIR")"

for dir in waybar wofi swaylock dunst kitty neofetch fastfetch; do
    target="$CONFIG_DIR/$dir"
    if [ -L "$target" ]; then
        rm "$target"
    elif [ -d "$target" ]; then
        echo "ВНИМАНИЕ: $target уже существует (не симлинк), пропускаю. Удалите вручную."
        continue
    fi
    ln -s "$HYPR_DIR/$dir" "$target"
    echo "$target -> $HYPR_DIR/$dir"
done

echo ""
echo "Проверка зависимостей для Theme Manager..."
if python3 -c "from PIL import Image" 2>/dev/null; then
    echo "  Pillow — OK"
else
    echo "  Pillow — НЕ НАЙДЕН (градиенты kitty не будут работать)"
    echo "  Установите: pip install Pillow"
fi

echo ""
echo "Готово!"
