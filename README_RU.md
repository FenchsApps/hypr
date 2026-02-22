# Hyprland Rice

Конфигурация Hyprland с кастомными темами, медиаплеером в waybar, настройкой neovim и oh-my-zsh.

**Автор:** FenchsApps

## Структура

```
hypr/
├── hyprland.conf          # Основной конфиг Hyprland
├── hyprpaper.conf         # Обои
├── waybar/                # Панель (конфиг + стили)
├── wofi/                  # Лаунчер приложений
├── kitty/                 # Терминал (+ градиентный фон)
├── dunst/                 # Уведомления
├── swaylock/              # Экран блокировки
├── nvim/                  # Конфиг Neovim (lazy.nvim + LSP)
├── fastfetch/             # Системная информация
├── neofetch/              # Системная информация (альт.)
├── hyfetch.json           # HyFetch (neofetch + флаги)
├── zshrc                  # Конфиг Zsh (симлинк на ~/.zshrc)
├── p10k.zsh               # Тема Powerlevel10k (симлинк на ~/.p10k.zsh)
├── gentoo-white.svg       # Иконка Gentoo (белая, исходник)
├── gentoo-icon.png        # Иконка Gentoo (генерируется при установке)
├── scripts/
│   ├── theme-manager.py   # GTK4 менеджер тем (3 темы)
│   ├── cheatsheet.py      # GTK4 шпаргалка по хоткеям
│   ├── float-at-cursor.sh # Плавающее окно под курсором
│   ├── cava-waybar.sh     # Визуализация звука в waybar
│   ├── terminal-name.sh   # Определение текущего терминала для waybar
│   ├── wallpaper.sh       # Выбор обоев через wofi
│   └── themes.json        # Определения тем
└── install.sh             # Полный установщик (симлинки + зависимости)
```

## Waybar

Округлённые pill-секции с прозрачным чёрным фоном. Иконка Gentoo слева, медиаплеер с кнопками управления по центру, системный трей с иконками приложений справа.

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

Скрипт выполнит:
- Создание симлинков в `~/.config/` для waybar, wofi, kitty, dunst, swaylock, neofetch, fastfetch, nvim
- Симлинк `zshrc` → `~/.zshrc` и `p10k.zsh` → `~/.p10k.zsh`
- Генерацию `gentoo-icon.png` из SVG
- Установку oh-my-zsh, powerlevel10k, zsh-autosuggestions, zsh-syntax-highlighting
- Установку плагинов neovim через lazy.nvim
- Проверку всех зависимостей

## Необходимые пакеты

### Основное

| Пакет | Описание |
|-------|----------|
| [hyprland](https://hyprland.org) | Wayland-композитор |
| [waybar](https://github.com/Alexays/Waybar) | Панель задач |
| [wofi](https://hg.sr.ht/~scoopta/wofi) | Лаунчер приложений |
| [kitty](https://sw.kovidgoyal.net/kitty/) | Эмулятор терминала |
| [dunst](https://dunst-project.org) | Демон уведомлений |
| [swaylock](https://github.com/swaywm/swaylock) | Экран блокировки |
| [hyprpaper](https://github.com/hyprwm/hyprpaper) | Менеджер обоев |

### Аудио

| Пакет | Описание |
|-------|----------|
| [pipewire](https://pipewire.org) | Аудио-сервер |
| wireplumber | Менеджер сессий PipeWire |
| pipewire-pulse | Совместимость с PulseAudio |
| [pavucontrol](https://freedesktop.org/software/pulseaudio/pavucontrol/) | GUI управления звуком |
| [playerctl](https://github.com/altdesktop/playerctl) | Управление медиаплеером (плеер в waybar) |
| [cava](https://github.com/karlstav/cava) | Визуализатор аудио |

### Сеть и Bluetooth

| Пакет | Описание |
|-------|----------|
| [networkmanager](https://networkmanager.dev) | Управление сетью |
| nm-applet | Трей-апплет NetworkManager |
| [blueman](https://github.com/blueman-project/blueman) | Bluetooth-менеджер |

### Шелл и редактор

| Пакет | Описание |
|-------|----------|
| [zsh](https://www.zsh.org) | Шелл |
| [oh-my-zsh](https://ohmyz.sh) | Фреймворк Zsh (ставится через install.sh) |
| [powerlevel10k](https://github.com/romkatv/powerlevel10k) | Тема Zsh (ставится через install.sh) |
| [neovim](https://neovim.io) | Текстовый редактор |

### Утилиты

| Пакет | Описание |
|-------|----------|
| [grim](https://sr.ht/~emersion/grim/) | Скриншоты |
| [slurp](https://github.com/emersion/slurp) | Выбор области экрана |
| [wl-clipboard](https://github.com/bugaevc/wl-clipboard) | Буфер обмена (wl-copy) |
| [brightnessctl](https://github.com/Haikarainen/light) | Управление яркостью |
| [jq](https://jqlang.github.io/jq/) | Обработка JSON (для скриптов) |
| [librsvg](https://wiki.gnome.org/Projects/LibRsvg) | Конвертер SVG (rsvg-convert, для генерации иконки) |

### Системная информация

| Пакет | Описание |
|-------|----------|
| [fastfetch](https://github.com/fastfetch-cli/fastfetch) | Информация о системе |
| [neofetch](https://github.com/dylanaraps/neofetch) | Информация о системе (альт.) |
| [hyfetch](https://github.com/hykilpikonna/hyfetch) | Neofetch + прайд-флаги |

### Python

| Пакет | Описание |
|-------|----------|
| python3 | Среда выполнения (для GTK-скриптов) |
| python3-gtk4 | GTK4 bindings (`gi.repository`) |
| [pillow](https://python-pillow.org) | Обработка изображений (градиенты kitty) |

### Шрифты

| Пакет | Описание |
|-------|----------|
| [FiraCode Nerd Font](https://www.nerdfonts.com) | Основной шрифт UI и терминала |

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
