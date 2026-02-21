#!/bin/sh

addr="$(hyprctl activewindow -j | jq -r '.address')"
floating="$(hyprctl activewindow -j | jq -r '.floating')"

hyprctl dispatch togglefloating address:"$addr"

if [ "$floating" = "false" ]; then
    cursor="$(hyprctl cursorpos -j)"
    cx="$(echo "$cursor" | jq -r '.x')"
    cy="$(echo "$cursor" | jq -r '.y')"

    win="$(hyprctl activewindow -j)"
    ww="$(echo "$win" | jq -r '.size[0]')"
    wh="$(echo "$win" | jq -r '.size[1]')"

    nx=$((cx - ww / 2))
    ny=$((cy - wh / 2))

    hyprctl dispatch movewindowpixel exact "$nx $ny",address:"$addr"
fi
