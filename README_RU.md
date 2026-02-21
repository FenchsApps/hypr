# Hyprland Rice

Конфигурация Hyprland с тремя темами, кастомными скриптами и полной интеграцией всех компонентов.

**Автор:** FenchsApps

## Структура

```
hypr/
├── hyprland.conf          # Основной конфиг Hyprland
├── hyprpaper.conf         # Обои
├── waybar/                # Панель (конфиг + стили)
├── wofi/                  # Лаунчер приложений
├── kitty/                 # Терминал
├── dunst/                 # Уведомления
├── swaylock/              # Экран блокировки
├── fastfetch/             # Системная информация
├── neofetch/              # Системная информация (альт.)
├── hyfetch.json           # HyFetch (neofetch + флаги)
├── scripts/
│   ├── theme-manager.py   # GTK4 менеджер тем (3 темы)
│   ├── cheatsheet.py      # GTK4 шпаргалка по хоткеям
│   ├── float-at-cursor.sh # Плавающее окно под курсором
│   ├── cava-waybar.sh     # Визуализация звука в waybar
│   ├── wallpaper.sh       # Выбор обоев через wofi
│   └── themes.json        # Определения тем
└── install.sh             # Установка симлинков
```

## Темы

| Тема | Акцент |
|------|--------|
| Life is Green | `#39ff14` `#00e676` |
| Truth is Red | `#ff1744` `#ff5252` |
| I am Purple | `#b388ff` `#7c4dff` |

Переключение: `SUPER + SHIFT + T`

## Установка

```bash
git clone <repo> ~/.config/hypr
cd ~/.config/hypr
chmod +x install.sh
./install.sh
```

Скрипт создаст симлинки в `~/.config/` для waybar, wofi, kitty, dunst, swaylock, neofetch, fastfetch и hyfetch.

## Обязательные программы

### Основное
- [Hyprland](https://hyprland.org) — Wayland-композитор
- [Waybar](https://github.com/Alexays/Waybar) — панель
- [Wofi](https://hg.sr.ht/~scoopta/wofi) — лаунчер
- [Kitty](https://sw.kovidgoyal.net/kitty/) — терминал
- [Dunst](https://dunst-project.org) — уведомления
- [Swaylock](https://github.com/swaywm/swaylock) — блокировка экрана
- [Hyprpaper](https://github.com/hyprwm/hyprpaper) — обои

### Аудио
- [PipeWire](https://pipewire.org) + WirePlumber + pipewire-pulse
- [PavuControl](https://freedesktop.org/software/pulseaudio/pavucontrol/) — управление звуком
- [Cava](https://github.com/karlstav/cava) — визуализация аудио

### Bluetooth и сеть
- [Blueman](https://github.com/blueman-project/blueman) — Bluetooth-менеджер
- [NetworkManager](https://networkmanager.dev) + nm-applet

### Утилиты
- [grim](https://sr.ht/~emersion/grim/) + [slurp](https://github.com/emersion/slurp) — скриншоты
- [wl-clipboard](https://github.com/bugaevc/wl-clipboard) — буфер обмена
- [jq](https://jqlang.github.io/jq/) — парсинг JSON (скрипты)
- [brightnessctl](https://github.com/Haikarainen/light) — яркость

### Системная информация
- [Fastfetch](https://github.com/fastfetch-cli/fastfetch)
- [Neofetch](https://github.com/dylanaraps/neofetch)
- [HyFetch](https://github.com/hykilpikonna/hyfetch)

### Python (для скриптов)
- Python 3 + GTK4 (`gi.repository`)
- [Pillow](https://python-pillow.org) — градиенты для Kitty

### Шрифты
- [FiraCode Nerd Font](https://www.nerdfonts.com)

## Горячие клавиши

| Комбинация | Действие |
|------------|----------|
| `SUPER + Return` | Kitty |
| `SUPER + Q` | Google Chrome |
| `SUPER + D` | Wofi (лаунчер) |
| `SUPER + E` | Nautilus |
| `SUPER + X` | Закрыть окно |
| `SUPER + F` | Maximize |
| `SUPER + V` | Float |
| `SUPER + SHIFT + SPACE` | Float под курсором |
| `SUPER + SPACE` | Раскладка EN/RU |
| `SUPER + L` | Блокировка |
| `SUPER + W` | Обои |
| `SUPER + SHIFT + T` | Менеджер тем |
| `SUPER + SHIFT + H` | Шпаргалка |
| `SUPER + SHIFT + A` | PavuControl |
| `SUPER + SHIFT + B` | Blueman |
| `Print` | Скриншот |
