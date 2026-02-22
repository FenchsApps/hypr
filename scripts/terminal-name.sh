#!/bin/sh
# Outputs the name of the focused terminal window, or nothing if not a terminal
active_class=$(hyprctl activewindow -j 2>/dev/null | jq -r '.class // empty' 2>/dev/null)

case "$active_class" in
    kitty)          echo '{"text": " kitty", "class": "terminal"}';;
    Alacritty)      echo '{"text": " Alacritty", "class": "terminal"}';;
    foot)           echo '{"text": " foot", "class": "terminal"}';;
    org.wezfurlong.wezterm) echo '{"text": " WezTerm", "class": "terminal"}';;
    *)              echo '{"text": "", "class": "empty"}';;
esac
