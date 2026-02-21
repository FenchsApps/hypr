#!/bin/sh

bars="▁▂▃▄▅▆▇█"

cava_config="
[general]
bars = 12
framerate = 30
autosens = 1
sensitivity = 80

[input]
method = pipewire
source = auto

[output]
method = raw
raw_target = /dev/stdout
data_format = ascii
ascii_max_range = 7
"

echo "$cava_config" | cava -p /dev/stdin 2>/dev/null | while IFS=';' read -r line; do
    out=""
    rest="$line"
    while [ -n "$rest" ]; do
        val="${rest%%;*}"
        if [ "$rest" = "$val" ]; then
            rest=""
        else
            rest="${rest#*;}"
        fi
        case "$val" in
            0) out="${out}▁" ;; 1) out="${out}▂" ;; 2) out="${out}▃" ;;
            3) out="${out}▄" ;; 4) out="${out}▅" ;; 5) out="${out}▆" ;;
            6) out="${out}▇" ;; 7) out="${out}█" ;; *) out="${out}▁" ;;
        esac
    done
    echo "$out" || exit 0
done
