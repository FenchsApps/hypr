#!/usr/bin/env python3
import gi, os, re
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, Gdk, GLib

CONF = os.path.expanduser("~/.config/hypr/hyprland.conf")

CSS = """
window {
    background-color: rgba(14,10,26,0.92);
}
.title-label {
    font-family: "FiraCode Nerd Font", monospace;
    font-size: 28px;
    font-weight: bold;
    color: #b388ff;
    margin: 16px 0 8px 0;
}
.subtitle-label {
    font-family: "Comic Sans MS", sans-serif;
    font-size: 13px;
    color: #6a4488;
    margin-bottom: 12px;
}
.section-label {
    font-family: "FiraCode Nerd Font", monospace;
    font-size: 15px;
    font-weight: bold;
    color: #7c4dff;
    margin: 12px 8px 6px 8px;
}
.bind-box {
    margin: 2px 8px;
    padding: 6px 12px;
    border-radius: 8px;
    background-color: rgba(255, 255, 255, 0.04);
}
.bind-box:hover {
    background-color: rgba(179,136,255,0.12);
}
.key-label {
    font-family: "FiraCode Nerd Font", monospace;
    font-size: 14px;
    font-weight: bold;
    color: #b388ff;
    min-width: 240px;
}
.desc-label {
    font-family: "Comic Sans MS", sans-serif;
    font-size: 13px;
    color: #e1bee7;
}
.search-entry {
    font-family: "Comic Sans MS", sans-serif;
    font-size: 14px;
    background-color: rgba(255, 255, 255, 0.06);
    color: #ffffff;
    border: 1px solid rgba(179,136,255,0.3);
    border-radius: 10px;
    padding: 6px 12px;
    margin: 0 8px 8px 8px;
}
.search-entry:focus {
    border-color: #b388ff;
}
.hint-label {
    font-family: "Comic Sans MS", sans-serif;
    font-size: 11px;
    color: #6a4488;
    margin: 4px 0 12px 0;
}
""".strip()

KEY_NAMES = {
    "Return": "Enter", "space": "Space", "Tab": "Tab",
    "left": "←", "right": "→", "up": "↑", "down": "↓",
    "mouse_down": "Scroll ↓", "mouse_up": "Scroll ↑",
    "mouse:272": "LMB", "mouse:273": "RMB",
    "Print": "PrtSc",
    "XF86AudioRaiseVolume": "Vol +", "XF86AudioLowerVolume": "Vol −",
    "XF86AudioMute": "Mute", "XF86AudioMicMute": "Mic Mute",
    "XF86MonBrightnessUp": "Bright +", "XF86MonBrightnessDown": "Bright −",
}

def fmt_key(mods, key):
    parts = []
    m = mods.strip().upper()
    if m:
        for tok in m.split():
            if tok == "SUPER":
                parts.append("󰖳")
            elif tok == "SHIFT":
                parts.append("⇧")
            elif tok == "CTRL":
                parts.append("Ctrl")
            elif tok == "ALT":
                parts.append("Alt")
            else:
                parts.append(tok)
    parts.append(KEY_NAMES.get(key.strip(), key.strip().upper()))
    return "  +  ".join(parts)


def parse_config(path):
    sections = []
    current_section = None
    current_binds = []
    comment_desc = None

    bind_re = re.compile(
        r'^bind[eidnmrl]*\s*=\s*'
        r'([^,]*),\s*'       # mods
        r'([^,]+),\s*'       # key
        r'(\S+)'             # dispatcher
        r'(?:\s*,\s*(.*))?'  # args
    )
    section_re = re.compile(r'^#\s*│\s*(.+?)\s*│\s*$')

    with open(path) as f:
        for raw_line in f:
            line = raw_line.rstrip()

            sm = section_re.match(line)
            if sm:
                name = sm.group(1).strip()
                if name.startswith("KEYBINDS"):
                    if current_section and current_binds:
                        sections.append((current_section, current_binds))
                    current_section = name.replace("ГОРЯЧИЕ КЛАВИШИ — ", "").replace("ГОРЯЧИЕ КЛАВИШИ —", "").strip()
                    current_binds = []
                continue

            if line.startswith("#") and current_section is not None:
                stripped = line.lstrip("# ").strip()
                if "→" in stripped:
                    comment_desc = stripped.split("→", 1)[1].strip()
                elif stripped and not stripped.startswith("┌") and not stripped.startswith("└") and not stripped.startswith("│"):
                    comment_desc = stripped
                continue

            bm = bind_re.match(line)
            if bm and current_section is not None:
                mods, key, dispatcher, args = bm.group(1), bm.group(2), bm.group(3), bm.group(4) or ""
                display_key = fmt_key(mods, key)

                if comment_desc:
                    desc = comment_desc
                else:
                    desc_map = {
                        "killactive": "Close window",
                        "togglefloating": "Toggle floating",
                        "pseudo": "Pseudo-tiling",
                        "togglesplit": "Toggle split",
                        "fullscreen": "Fullscreen",
                        "movewindow": f"Move window ({args})",
                        "movefocus": f"Focus ({args})",
                        "workspace": f"Workspace {args}",
                        "movetoworkspace": f"Window → workspace {args}",
                        "resizeactive": f"Resize ({args})",
                        "cyclenext": "Next window",
                        "exit": "Exit Hyprland",
                        "togglespecialworkspace": "Scratchpad",
                        "movewindow": f"Move ({args})",
                        "centerwindow": "Center window",
                    }
                    desc = desc_map.get(dispatcher, f"{dispatcher} {args}".strip())

                current_binds.append((display_key, desc))
                comment_desc = None
            else:
                if not line.strip() or line.startswith("#"):
                    pass
                else:
                    comment_desc = None

    if current_section and current_binds:
        sections.append((current_section, current_binds))

    return sections


class CheatSheet(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="hypr.cheatsheet")
        self.sections = parse_config(CONF)

    def do_activate(self):
        css_prov = Gtk.CssProvider()
        css_prov.load_from_string(CSS)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css_prov,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        win = Gtk.ApplicationWindow(application=self, title="Hyprland Cheatsheet")
        win.set_default_size(680, 820)

        esc = Gtk.EventControllerKey()
        esc.connect("key-pressed", self._on_key, win)
        win.add_controller(esc)

        root_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        win.set_child(root_box)

        title = Gtk.Label(label="  Hyprland Binds")
        title.add_css_class("title-label")
        root_box.append(title)

        sub = Gtk.Label(label="~ I am Purple Cheatsheet ~")
        sub.add_css_class("subtitle-label")
        root_box.append(sub)

        self.search = Gtk.SearchEntry(placeholder_text="Поиск...")
        self.search.add_css_class("search-entry")
        self.search.connect("search-changed", self._on_search)
        root_box.append(self.search)

        hint = Gtk.Label(label="ESC — close")
        hint.add_css_class("hint-label")
        root_box.append(hint)

        scroll = Gtk.ScrolledWindow(vexpand=True, hscrollbar_policy=Gtk.PolicyType.NEVER)
        root_box.append(scroll)

        self.content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        scroll.set_child(self.content)

        self.bind_widgets = []
        self._build_sections()

        win.present()

    def _build_sections(self):
        for section_name, binds in self.sections:
            sec_label = Gtk.Label(label=f"  {section_name}", xalign=0)
            sec_label.add_css_class("section-label")
            self.content.append(sec_label)

            for key_str, desc in binds:
                row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
                row.add_css_class("bind-box")

                kl = Gtk.Label(label=key_str, xalign=0)
                kl.add_css_class("key-label")
                row.append(kl)

                dl = Gtk.Label(label=desc, xalign=0, hexpand=True)
                dl.add_css_class("desc-label")
                row.append(dl)

                self.content.append(row)
                self.bind_widgets.append((sec_label, row, key_str, desc))

    def _on_search(self, entry):
        query = entry.get_text().lower()
        visible_sections = set()
        for sec_label, row, key_str, desc in self.bind_widgets:
            match = not query or query in key_str.lower() or query in desc.lower()
            row.set_visible(match)
            if match:
                visible_sections.add(sec_label)
        for sec_label, _, _, _ in self.bind_widgets:
            sec_label.set_visible(sec_label in visible_sections)

    def _on_key(self, ctrl, keyval, keycode, state, win):
        if keyval == Gdk.KEY_Escape:
            win.close()
            return True
        return False


if __name__ == "__main__":
    app = CheatSheet()
    app.run()
