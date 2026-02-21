#!/usr/bin/env python3
import gi, os, json, subprocess, re
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, Gdk

HYPR_DIR = os.path.expanduser("~/.config/hypr")
THEMES_FILE = os.path.join(HYPR_DIR, "scripts/themes.json")
STATE_FILE = os.path.join(HYPR_DIR, "scripts/.theme-state.json")

def load_themes():
    with open(THEMES_FILE) as f:
        return json.load(f)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"active": "life_is_green", "kitty_bg_mode": "solid", "kitty_gradient_dir": "vertical", "border_mode": "loop", "kitty_fg_color": ""}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ── Config generators ──────────────────────────────────────────────

def hex_to_rgba(h, alpha="ff"):
    """For Hyprland config: rgba(rrggbbaa)"""
    h = h.lstrip("#")
    return f"rgba({h}{alpha})"

def css_rgba(h, alpha_hex):
    """Convert #rrggbb + 2-char hex alpha to CSS rgba(r,g,b,a)"""
    h = h.lstrip("#")
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    a = round(int(alpha_hex, 16) / 255, 2)
    return f"rgba({r},{g},{b},{a})"

def generate_hyprland_colors(t, border_mode):
    cmds = [
        f'hyprctl keyword general:col.active_border "{hex_to_rgba(t["accent"])} {hex_to_rgba(t["accent2"])} 45deg"',
        f'hyprctl keyword general:col.inactive_border "{hex_to_rgba(t["muted"], "40")}"',
        f'hyprctl keyword decoration:shadow:color "{hex_to_rgba(t["accent"], "55")}"',
        f'hyprctl keyword decoration:shadow:color_inactive "{hex_to_rgba(t["bg"], "66")}"',
    ]
    if border_mode == "loop":
        cmds.append('hyprctl keyword animation "borderangle, 1, 100, liner, loop"')
    elif border_mode == "once":
        cmds.append('hyprctl keyword animation "borderangle, 1, 100, liner, once"')
    else:
        cmds.append('hyprctl keyword animation "borderangle, 0, 0, default"')
    for cmd in cmds:
        subprocess.run(cmd, shell=True, capture_output=True)

def generate_waybar_style(t):
    css = f'''* {{
    font-family: "Comic Sans MS", "Comic Neue", sans-serif;
    font-size: 14px;
    color: #ffffff;
    border: none;
    border-radius: 0;
    min-height: 0;
}}

window#waybar {{
    background: {css_rgba(t["bg"],"e0")};
    border-radius: 16px;
    border: 1px solid {css_rgba(t["accent"],"26")};
}}

tooltip {{
    background: {css_rgba(t["bg"],"eb")};
    border: 1px solid {css_rgba(t["accent"],"4d")};
    border-radius: 12px;
    color: #ffffff;
}}

tooltip label {{
    color: #ffffff;
}}

#custom-gentoo {{
    font-family: "FiraCode Nerd Font", sans-serif;
    font-size: 20px;
    color: {t["muted"]};
    padding: 0 6px 0 14px;
    margin: 4px 0;
}}

#custom-gentoo:hover {{
    color: {t["accent"]};
}}

#workspaces {{
    padding: 0 6px;
    margin: 4px 0;
}}

#workspaces button {{
    font-family: "Comic Sans MS", "Comic Neue", sans-serif;
    font-size: 13px;
    font-weight: bold;
    color: #ffffff;
    background: transparent;
    border: 2px solid rgba(255, 255, 255, 0.7);
    border-radius: 10px;
    padding: 2px 10px;
    margin: 2px 3px;
    min-width: 28px;
}}

#workspaces button:hover {{
    background: rgba(255, 255, 255, 0.08);
    border-color: {t["accent"]};
    color: {t["accent"]};
}}

#workspaces button.active {{
    color: {t["active"]};
    background: {css_rgba(t["accent"],"40")};
    border: 2px solid transparent;
}}

#workspaces button.urgent {{
    color: #ff0000;
    background: rgba(255, 0, 0, 0.2);
    border-color: #ff0000;
}}

#clock {{
    font-family: "Comic Sans MS", "Comic Neue", sans-serif;
    font-size: 14px;
    font-weight: bold;
    color: {t["fg"]};
    padding: 0 14px;
    margin: 4px 0;
}}

#custom-cava {{
    font-size: 12px;
    color: {t["accent"]};
    padding: 0 12px;
    margin: 4px 0;
    letter-spacing: -1px;
}}

#bluetooth {{
    padding: 0 10px;
    margin: 4px 0;
    color: {t["fg"]};
}}

#bluetooth:hover {{
    color: {t["accent"]};
}}

#bluetooth.connected {{
    color: {t["accent"]};
}}

#bluetooth.disabled {{
    color: {t["muted2"]};
}}

#pulseaudio {{
    padding: 0 14px 0 10px;
    margin: 4px 8px 4px 4px;
    color: {t["fg"]};
}}

#pulseaudio:hover {{
    color: {t["accent"]};
}}

#pulseaudio.muted {{
    color: {t["muted2"]};
}}
'''
    with open(os.path.join(HYPR_DIR, "waybar/style.css"), "w") as f:
        f.write(css)

def generate_waybar_calendar_colors(t):
    path = os.path.join(HYPR_DIR, "waybar/config.jsonc")
    with open(path) as f:
        content = f.read()
    content = re.sub(r"<span color='#[0-9a-fA-F]{6}'><b>\{\}</b></span>",
                     f"<span color='{t['accent']}'><b>{{}}</b></span>", content)
    content = re.sub(r"<span color='#[0-9a-fA-F]{6}'><b><u>\{\}</u></b></span>",
                     f"<span color='{t['active']}'><b><u>{{}}</u></b></span>", content)
    with open(path, "w") as f:
        f.write(content)

def generate_wofi_style(t):
    css = f'''window {{
    margin: 0px;
    border: 5px solid {t["accent"]};
    background-color: {t["accent"]};
    border-radius: 15px;
}}

#input {{
    padding: 4px;
    margin: 4px;
    padding-left: 20px;
    border: none;
    color: #fff;
    font-weight: bold;
    background-color: #fff;
    background: linear-gradient(90deg, {t["muted"]} 0%, {t["accent"]} 100%);
    outline: none;
    border-radius: 15px;
    margin: 10px;
    margin-bottom: 2px;
}}
#input:focus {{
    border: 0px solid #fff;
    margin-bottom: 0px;
}}

#inner-box {{
    margin: 4px;
    border: 10px solid #fff;
    color: {t["muted"]};
    font-weight: bold;
    background-color: #fff;
    border-radius: 15px;
}}

#outer-box {{
    margin: 0px;
    border: none;
    border-radius: 15px;
    background-color: #fff;
}}

#scroll {{
    margin-top: 5px;
    border: none;
    border-radius: 15px;
    margin-bottom: 5px;
}}

#text:selected {{
    color: #fff;
    margin: 0px 0px;
    border: none;
    border-radius: 15px;
}}

#entry {{
    margin: 0px 0px;
    border: none;
    border-radius: 15px;
    background-color: transparent;
}}

#entry:selected {{
    margin: 0px 0px;
    border: none;
    border-radius: 15px;
    background: linear-gradient(45deg, {t["muted"]} 30%, {t["accent"]} 100%);
}}
'''
    with open(os.path.join(HYPR_DIR, "wofi/style.css"), "w") as f:
        f.write(css)

def generate_swaylock_config(t):
    cfg = f'''daemonize
show-failed-attempts
clock
effect-blur=5x5
color={t["bg"].lstrip("#")}80
font="Inter"
indicator
indicator-radius=200
indicator-thickness=20
line-color={t["bg"].lstrip("#")}
ring-color={t["bg2"].lstrip("#")}
inside-color={t["bg"].lstrip("#")}
key-hl-color={t["accent"].lstrip("#")}
separator-color=00000000
text-color={t["fg"].lstrip("#")}
text-caps-lock-color=""
line-ver-color={t["accent"].lstrip("#")}
ring-ver-color={t["accent"].lstrip("#")}
inside-ver-color={t["bg"].lstrip("#")}
text-ver-color={t["fg"].lstrip("#")}
ring-wrong-color={t["error"].lstrip("#")}
text-wrong-color={t["error"].lstrip("#")}
inside-wrong-color={t["bg"].lstrip("#")}
inside-clear-color={t["bg"].lstrip("#")}
text-clear-color={t["fg"].lstrip("#")}
ring-clear-color={t["accent2"].lstrip("#")}
line-clear-color={t["bg"].lstrip("#")}
line-wrong-color={t["bg"].lstrip("#")}
bs-hl-color={t["error"].lstrip("#")}
grace=2
grace-no-mouse
grace-no-touch
datestr="%d.%m"
fade-in="0.1"
ignore-empty-password
'''
    with open(os.path.join(HYPR_DIR, "swaylock/config"), "w") as f:
        f.write(cfg)

def generate_kitty_conf(t, bg_mode, gradient_dir, gradient_from, gradient_to, fg_color=""):
    tc = t["terminal_colors"]
    bg_image_line = ""
    bg_color = t["bg"]
    fg = fg_color if fg_color else t["fg"]
    if bg_mode == "gradient":
        png_path = os.path.join(HYPR_DIR, "kitty/gradient.png")
        _generate_gradient_png(gradient_from, gradient_to, gradient_dir, png_path)
        bg_image_line = f"background_image {png_path}\nbackground_image_layout scaled"

    conf = f'''font_family      FiraCode Nerd Font
bold_font        FiraCode Nerd Font Bold
italic_font      auto
bold_italic_font auto
font_size        10.0

background_opacity 0.82
background {bg_color}
{bg_image_line}

foreground {fg}
cursor     {t["accent"]}
cursor_text_color {t["bg"]}

selection_foreground {t["bg"]}
selection_background {t["accent"]}

color0  {tc["color0"]}
color8  {tc["color8"]}

color1  {tc["color1"]}
color9  {tc["color9"]}

color2  {tc["color2"]}
color10 {tc["color10"]}

color3  {tc["color3"]}
color11 {tc["color11"]}

color4  {tc["color4"]}
color12 {tc["color12"]}

color5  {tc["color5"]}
color13 {tc["color13"]}

color6  {tc["color6"]}
color14 {tc["color14"]}

color7  {tc["color7"]}
color15 {tc["color15"]}

url_color {t["accent2"]}
url_style curly

active_border_color   {t["accent"]}
inactive_border_color {t["muted"]}
bell_border_color     {t["active"]}

active_tab_foreground   {t["bg"]}
active_tab_background   {t["accent"]}
active_tab_font_style   bold
inactive_tab_foreground {t["fg"]}
inactive_tab_background {t["bg2"]}
inactive_tab_font_style normal
tab_bar_style           powerline
tab_powerline_style     slanted

window_padding_width 6
confirm_os_window_close 0

enable_audio_bell no
'''
    with open(os.path.join(HYPR_DIR, "kitty/kitty.conf"), "w") as f:
        f.write(conf)

def _generate_gradient_png(color_from, color_to, direction, path):
    try:
        from PIL import Image
    except ImportError:
        return
    w, h = 1920, 1080
    r1, g1, b1 = int(color_from[1:3],16), int(color_from[3:5],16), int(color_from[5:7],16)
    r2, g2, b2 = int(color_to[1:3],16), int(color_to[3:5],16), int(color_to[5:7],16)
    img = Image.new("RGB", (w, h))
    pixels = img.load()
    for y in range(h):
        for x in range(w):
            if direction == "vertical":
                ratio = y / (h - 1)
            else:
                ratio = x / (w - 1)
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            pixels[x, y] = (r, g, b)
    img.save(path)

def generate_cheatsheet_css(t):
    path = os.path.join(HYPR_DIR, "scripts/cheatsheet.py")
    with open(path) as f:
        content = f.read()

    new_css = f'''CSS = """
window {{
    background-color: {css_rgba(t["bg"],"eb")};
}}
.title-label {{
    font-family: "FiraCode Nerd Font", monospace;
    font-size: 28px;
    font-weight: bold;
    color: {t["accent"]};
    margin: 16px 0 8px 0;
}}
.subtitle-label {{
    font-family: "Comic Sans MS", sans-serif;
    font-size: 13px;
    color: {t["muted2"]};
    margin-bottom: 12px;
}}
.section-label {{
    font-family: "FiraCode Nerd Font", monospace;
    font-size: 15px;
    font-weight: bold;
    color: {t["accent2"]};
    margin: 12px 8px 6px 8px;
}}
.bind-box {{
    margin: 2px 8px;
    padding: 6px 12px;
    border-radius: 8px;
    background-color: rgba(255, 255, 255, 0.04);
}}
.bind-box:hover {{
    background-color: {css_rgba(t["accent"],"1f")};
}}
.key-label {{
    font-family: "FiraCode Nerd Font", monospace;
    font-size: 14px;
    font-weight: bold;
    color: {t["accent"]};
    min-width: 240px;
}}
.desc-label {{
    font-family: "Comic Sans MS", sans-serif;
    font-size: 13px;
    color: {t["fg"]};
}}
.search-entry {{
    font-family: "Comic Sans MS", sans-serif;
    font-size: 14px;
    background-color: rgba(255, 255, 255, 0.06);
    color: #ffffff;
    border: 1px solid {css_rgba(t["accent"],"4d")};
    border-radius: 10px;
    padding: 6px 12px;
    margin: 0 8px 8px 8px;
}}
.search-entry:focus {{
    border-color: {t["accent"]};
}}
.hint-label {{
    font-family: "Comic Sans MS", sans-serif;
    font-size: 11px;
    color: {t["muted2"]};
    margin: 4px 0 12px 0;
}}
""".strip()'''

    content = re.sub(r'CSS = """.*?""".strip\(\)', new_css, content, flags=re.DOTALL)

    theme_label = t["name"]
    content = re.sub(
        r'sub = Gtk\.Label\(label="~ .+ Cheatsheet ~"\)',
        f'sub = Gtk.Label(label="~ {theme_label} Cheatsheet ~")',
        content
    )
    with open(path, "w") as f:
        f.write(content)

def generate_dunst_colors(t):
    path = os.path.join(HYPR_DIR, "dunst/dunstrc")
    with open(path) as f:
        content = f.read()
    content = re.sub(r'(frame_color\s*=\s*)"#[0-9a-fA-F]+"', f'\\1"{t["accent"]}"', content)

    content = re.sub(
        r'(\[urgency_low\].*?background\s*=\s*)"#[0-9a-fA-F]+"',
        f'\\1"{t["bg"]}"', content, flags=re.DOTALL)
    content = re.sub(
        r'(\[urgency_low\].*?foreground\s*=\s*)"#[0-9a-fA-F]+"',
        f'\\1"{t["muted2"]}"', content, flags=re.DOTALL)

    content = re.sub(
        r'(\[urgency_normal\].*?background\s*=\s*)"#[0-9a-fA-F]+"',
        f'\\1"{t["bg2"]}"', content, flags=re.DOTALL)
    content = re.sub(
        r'(\[urgency_normal\].*?foreground\s*=\s*)"#[0-9a-fA-F]+"',
        f'\\1"{t["fg2"]}"', content, flags=re.DOTALL)

    content = re.sub(
        r'(\[urgency_critical\].*?background\s*=\s*)"#[0-9a-fA-F]+"',
        f'\\1"{t["error"]}"', content, flags=re.DOTALL)
    content = re.sub(
        r'(\[urgency_critical\].*?foreground\s*=\s*)"#[0-9a-fA-F]+"',
        f'\\1"{t["fg2"]}"', content, flags=re.DOTALL)
    content = re.sub(
        r'(\[urgency_critical\].*?frame_color\s*=\s*)"#[0-9a-fA-F]+"',
        f'\\1"{t["error"]}"', content, flags=re.DOTALL)

    with open(path, "w") as f:
        f.write(content)

def reload_services():
    subprocess.run("killall waybar 2>/dev/null; sleep 0.3; waybar > /tmp/waybar.log 2>&1 &", shell=True)
    subprocess.run("killall dunst 2>/dev/null; sleep 0.3; dunst &", shell=True)


def apply_theme(theme_id, themes, kitty_bg_mode, kitty_gradient_dir, border_mode, kitty_fg_color=""):
    t = themes[theme_id]
    generate_hyprland_colors(t, border_mode)
    generate_waybar_style(t)
    generate_waybar_calendar_colors(t)
    generate_wofi_style(t)
    generate_swaylock_config(t)
    generate_kitty_conf(t, kitty_bg_mode, kitty_gradient_dir,
                        t["kitty_gradient_from"], t["kitty_gradient_to"], kitty_fg_color)
    generate_cheatsheet_css(t)
    generate_dunst_colors(t)
    reload_services()

    state = {
        "active": theme_id,
        "kitty_bg_mode": kitty_bg_mode,
        "kitty_gradient_dir": kitty_gradient_dir,
        "border_mode": border_mode,
        "kitty_fg_color": kitty_fg_color
    }
    save_state(state)


# ── GTK4 UI ────────────────────────────────────────────────────────

def build_css(t):
    return f"""
window {{
    background-color: {css_rgba(t["bg"],"eb")};
}}
.app-title {{
    font-family: "FiraCode Nerd Font", monospace;
    font-size: 24px;
    font-weight: bold;
    color: {t["accent"]};
    margin: 14px 0 4px 0;
}}
.app-subtitle {{
    font-family: "Comic Sans MS", sans-serif;
    font-size: 12px;
    color: {t["muted2"]};
    margin-bottom: 10px;
}}
.section-title {{
    font-family: "FiraCode Nerd Font", monospace;
    font-size: 13px;
    font-weight: bold;
    color: {t["accent2"]};
    margin: 10px 12px 4px 12px;
}}
.theme-card {{
    border-radius: 12px;
    padding: 10px 16px;
    margin: 4px 12px;
    background-color: rgba(255,255,255,0.04);
    border: 2px solid transparent;
}}
.theme-card:hover {{
    background-color: rgba(255,255,255,0.08);
}}
.theme-card-active {{
    border: 2px solid {t["accent"]};
    background-color: {css_rgba(t["accent"],"1a")};
}}
.theme-name {{
    font-family: "Comic Sans MS", sans-serif;
    font-size: 15px;
    font-weight: bold;
    color: {t["fg"]};
}}
.color-dot {{
    min-width: 18px;
    min-height: 18px;
    border-radius: 9px;
}}
.option-label {{
    font-family: "Comic Sans MS", sans-serif;
    font-size: 13px;
    color: {t["fg"]};
    margin: 0 12px;
}}
.apply-btn {{
    font-family: "Comic Sans MS", sans-serif;
    font-size: 15px;
    font-weight: bold;
    color: {t["bg"]};
    background-color: {t["accent"]};
    border: none;
    border-radius: 12px;
    padding: 10px 24px;
    margin: 12px 40px;
}}
.apply-btn:hover {{
    background-color: {t["active"]};
}}
.hint {{
    font-family: "Comic Sans MS", sans-serif;
    font-size: 11px;
    color: {t["muted2"]};
    margin: 0 0 10px 0;
}}
checkbutton label {{
    color: {t["fg"]};
    font-family: "Comic Sans MS", sans-serif;
    font-size: 13px;
}}
checkbutton radio {{
    color: {t["accent"]};
}}
.color-entry {{
    font-family: "FiraCode Nerd Font", monospace;
    font-size: 13px;
    background-color: rgba(255,255,255,0.06);
    color: {t["fg"]};
    border: 1px solid {css_rgba(t["accent"],"4d")};
    border-radius: 8px;
    padding: 4px 10px;
    min-width: 100px;
}}
.color-entry:focus {{
    border-color: {t["accent"]};
}}
.color-preview {{
    min-width: 24px;
    min-height: 24px;
    border-radius: 6px;
    border: 1px solid rgba(255,255,255,0.2);
}}
"""

class ThemeManager(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="hypr.thememanager")
        self.themes = load_themes()
        self.state = load_state()
        self.selected_theme = self.state["active"]
        self.kitty_bg_mode = self.state.get("kitty_bg_mode", "solid")
        self.kitty_gradient_dir = self.state.get("kitty_gradient_dir", "vertical")
        self.border_mode = self.state.get("border_mode", "loop")
        self.kitty_fg_color = self.state.get("kitty_fg_color", "")
        self.card_widgets = {}

    def do_activate(self):
        t = self.themes[self.selected_theme]
        css_prov = Gtk.CssProvider()
        css_prov.load_from_string(build_css(t))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css_prov,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.css_prov = css_prov

        win = Gtk.ApplicationWindow(application=self, title="Theme Manager")
        win.set_default_size(520, 640)

        esc = Gtk.EventControllerKey()
        esc.connect("key-pressed", self._on_key, win)
        win.add_controller(esc)

        scroll = Gtk.ScrolledWindow(hscrollbar_policy=Gtk.PolicyType.NEVER, vexpand=True)
        win.set_child(scroll)

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        scroll.set_child(root)

        title = Gtk.Label(label="  Theme Manager")
        title.add_css_class("app-title")
        root.append(title)

        sub = Gtk.Label(label="Выбери тему, настрой и применяй")
        sub.add_css_class("app-subtitle")
        root.append(sub)

        # ── Theme cards ──
        sec = Gtk.Label(label="  ТЕМА", xalign=0)
        sec.add_css_class("section-title")
        root.append(sec)

        for tid, tdata in self.themes.items():
            card = self._make_theme_card(tid, tdata)
            root.append(card)
            self.card_widgets[tid] = card

        self._update_card_styles()

        # ── Kitty background ──
        sec2 = Gtk.Label(label="  KITTY ФОН", xalign=0)
        sec2.add_css_class("section-title")
        root.append(sec2)

        bg_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        bg_box.set_margin_start(16)
        bg_box.set_margin_top(4)
        self.radio_solid = Gtk.CheckButton(label="Статичный цвет")
        self.radio_gradient = Gtk.CheckButton(label="Градиент")
        self.radio_gradient.set_group(self.radio_solid)
        if self.kitty_bg_mode == "gradient":
            self.radio_gradient.set_active(True)
        else:
            self.radio_solid.set_active(True)
        self.radio_solid.connect("toggled", self._on_kitty_bg_toggle)
        bg_box.append(self.radio_solid)
        bg_box.append(self.radio_gradient)
        root.append(bg_box)

        self.grad_dir_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        self.grad_dir_box.set_margin_start(16)
        self.grad_dir_box.set_margin_top(4)
        self.radio_vert = Gtk.CheckButton(label="Вертикальный")
        self.radio_horiz = Gtk.CheckButton(label="Горизонтальный")
        self.radio_horiz.set_group(self.radio_vert)
        if self.kitty_gradient_dir == "horizontal":
            self.radio_horiz.set_active(True)
        else:
            self.radio_vert.set_active(True)
        self.radio_vert.connect("toggled", self._on_grad_dir_toggle)
        self.grad_dir_box.append(self.radio_vert)
        self.grad_dir_box.append(self.radio_horiz)
        self.grad_dir_box.set_visible(self.kitty_bg_mode == "gradient")
        root.append(self.grad_dir_box)

        # ── Kitty font color ──
        sec_fg = Gtk.Label(label="  ЦВЕТ ШРИФТА KITTY", xalign=0)
        sec_fg.add_css_class("section-title")
        root.append(sec_fg)

        fg_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        fg_box.set_margin_start(16)
        fg_box.set_margin_top(4)
        fg_box.set_margin_bottom(4)

        fg_hint = Gtk.Label(label="HEX:", xalign=0)
        fg_hint.add_css_class("option-label")
        fg_box.append(fg_hint)

        self.fg_entry = Gtk.Entry()
        self.fg_entry.add_css_class("color-entry")
        self.fg_entry.set_placeholder_text(self.themes[self.selected_theme]["fg"])
        self.fg_entry.set_max_length(7)
        if self.kitty_fg_color:
            self.fg_entry.set_text(self.kitty_fg_color)
        self.fg_entry.connect("changed", self._on_fg_entry_changed)
        fg_box.append(self.fg_entry)

        self.fg_preview = Gtk.DrawingArea()
        self.fg_preview.add_css_class("color-preview")
        self.fg_preview.set_content_width(24)
        self.fg_preview.set_content_height(24)
        self._update_fg_preview()
        fg_box.append(self.fg_preview)

        fg_reset = Gtk.Button(label="Сброс")
        fg_reset.connect("clicked", self._on_fg_reset)
        fg_box.append(fg_reset)

        root.append(fg_box)

        # ── Border animation ──
        sec3 = Gtk.Label(label="  АНИМАЦИЯ БОРДЕРА", xalign=0)
        sec3.add_css_class("section-title")
        root.append(sec3)

        border_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        border_box.set_margin_start(16)
        border_box.set_margin_top(4)
        self.radio_loop = Gtk.CheckButton(label="Loop")
        self.radio_once = Gtk.CheckButton(label="Once")
        self.radio_static = Gtk.CheckButton(label="Статичный")
        self.radio_once.set_group(self.radio_loop)
        self.radio_static.set_group(self.radio_loop)
        if self.border_mode == "once":
            self.radio_once.set_active(True)
        elif self.border_mode == "static":
            self.radio_static.set_active(True)
        else:
            self.radio_loop.set_active(True)
        self.radio_loop.connect("toggled", self._on_border_toggle)
        self.radio_once.connect("toggled", self._on_border_toggle)
        self.radio_static.connect("toggled", self._on_border_toggle)
        border_box.append(self.radio_loop)
        border_box.append(self.radio_once)
        border_box.append(self.radio_static)
        root.append(border_box)

        # ── Apply button ──
        apply_btn = Gtk.Button(label="  Применить")
        apply_btn.add_css_class("apply-btn")
        apply_btn.connect("clicked", self._on_apply)
        root.append(apply_btn)

        hint = Gtk.Label(label="ESC — закрыть  |  Применяется ко всем конфигам")
        hint.add_css_class("hint")
        root.append(hint)

        win.present()

    def _make_theme_card(self, tid, tdata):
        card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        card.add_css_class("theme-card")

        gesture = Gtk.GestureClick()
        gesture.connect("released", self._on_card_click, tid)
        card.add_controller(gesture)

        name_label = Gtk.Label(label=tdata["name"], xalign=0, hexpand=True)
        name_label.add_css_class("theme-name")
        card.append(name_label)

        for color_key in ["accent", "accent2", "active", "bg"]:
            dot = Gtk.DrawingArea()
            dot.add_css_class("color-dot")
            dot.set_content_width(18)
            dot.set_content_height(18)
            c = tdata[color_key]
            r = int(c[1:3],16)/255
            g = int(c[3:5],16)/255
            b = int(c[5:7],16)/255
            dot.set_draw_func(self._draw_dot, (r, g, b))
            card.append(dot)

        return card

    @staticmethod
    def _draw_dot(area, cr, w, h, color):
        r, g, b = color
        cr.arc(w/2, h/2, min(w,h)/2, 0, 6.283185)
        cr.set_source_rgb(r, g, b)
        cr.fill()

    def _on_card_click(self, gesture, n_press, x, y, tid):
        self.selected_theme = tid
        self._update_card_styles()
        t = self.themes[tid]
        self.css_prov.load_from_string(build_css(t))

    def _update_card_styles(self):
        for tid, card in self.card_widgets.items():
            if tid == self.selected_theme:
                card.add_css_class("theme-card-active")
            else:
                card.remove_css_class("theme-card-active")

    def _on_kitty_bg_toggle(self, btn):
        if self.radio_solid.get_active():
            self.kitty_bg_mode = "solid"
        else:
            self.kitty_bg_mode = "gradient"
        self.grad_dir_box.set_visible(self.kitty_bg_mode == "gradient")

    def _on_grad_dir_toggle(self, btn):
        if self.radio_vert.get_active():
            self.kitty_gradient_dir = "vertical"
        else:
            self.kitty_gradient_dir = "horizontal"

    def _on_border_toggle(self, btn):
        if self.radio_loop.get_active():
            self.border_mode = "loop"
        elif self.radio_once.get_active():
            self.border_mode = "once"
        elif self.radio_static.get_active():
            self.border_mode = "static"

    def _on_fg_entry_changed(self, entry):
        text = entry.get_text().strip()
        if re.match(r'^#[0-9a-fA-F]{6}$', text):
            self.kitty_fg_color = text
            self._update_fg_preview()
        elif text == "":
            self.kitty_fg_color = ""
            self._update_fg_preview()

    def _on_fg_reset(self, btn):
        self.kitty_fg_color = ""
        self.fg_entry.set_text("")
        self._update_fg_preview()

    def _update_fg_preview(self):
        color = self.kitty_fg_color if self.kitty_fg_color else self.themes[self.selected_theme]["fg"]
        r = int(color[1:3],16)/255
        g = int(color[3:5],16)/255
        b = int(color[5:7],16)/255
        self.fg_preview.set_draw_func(self._draw_dot, (r, g, b))

    def _on_apply(self, btn):
        apply_theme(self.selected_theme, self.themes,
                    self.kitty_bg_mode, self.kitty_gradient_dir, self.border_mode,
                    self.kitty_fg_color)

    def _on_key(self, ctrl, keyval, keycode, state, win):
        if keyval == Gdk.KEY_Escape:
            win.close()
            return True
        return False


if __name__ == "__main__":
    app = ThemeManager()
    app.run()
