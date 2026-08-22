import os

import tkinter as tk
from tkinter import messagebox

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from models.department import Department


# =========================
# THEMES
# =========================

LIGHT_THEME = {
    "card_bg": "#FFFFFF",
    "body_bg": "#FFFFFF",
    "border": "#E5E9EB",
    "field_bg": "#F5F7F8",
    "field_border": "#E2E6E8",
    "placeholder": "#9AA5AA",
    "text": "#1F2933",
    "subtitle": "#8A949A",
    "icon_bg": "#E4F5F0",
    "accent": "#22A18C",
    "accent_hover": "#1C8A78",
    "accent_text": "#FFFFFF",
    "cancel_bg": "#FFFFFF",
    "cancel_border": "#E2E6E8",
    "cancel_text": "#4B5563",
    "footer_bg": "#FFFFFF",
    "close_bg": "#F1F3F4",
    "close_fg": "#5F6B70",
    "switch_track_on": "#22A18C",
    "switch_track_off": "#D7DCE0",
    "switch_knob": "#FFFFFF",
}

DARK_THEME = {
    "card_bg": "#111827",
    "body_bg": "#111827",
    "border": "#1F2A3A",
    "field_bg": "#182234",
    "field_border": "#26334A",
    "placeholder": "#5B6B80",
    "text": "#E8EDF2",
    "subtitle": "#7C8A9C",
    "icon_bg": "#123A34",
    "accent": "#20C9A6",
    "accent_hover": "#1BAE90",
    "accent_text": "#0B1220",
    "cancel_bg": "#111827",
    "cancel_border": "#26334A",
    "cancel_text": "#C4CDD8",
    "footer_bg": "#111827",
    "close_bg": "#1B2536",
    "close_fg": "#9AA7B5",
    "switch_track_on": "#20C9A6",
    "switch_track_off": "#2A3547",
    "switch_knob": "#0B1220",
}


class ToggleSwitch(tk.Canvas):
    """A small pill-shaped on/off switch, styled like the sidebar toggle."""

    def __init__(self, parent, command=None, width=46, height=24, **kwargs):
        super().__init__(
            parent, width=width, height=height,
            highlightthickness=0, bd=0, **kwargs
        )
        self.command = command
        self.width = width
        self.height = height
        self.is_on = False

        self.track_on = "#22A18C"
        self.track_off = "#D7DCE0"
        self.knob_color = "#FFFFFF"

        self.bind("<Button-1>", self._on_click)
        self.configure(cursor="hand2")
        self.draw()

    def set_colors(self, track_on, track_off, knob_color, bg):
        self.track_on = track_on
        self.track_off = track_off
        self.knob_color = knob_color
        self.configure(bg=bg)
        self.draw()

    def set_state(self, is_on, redraw=True):
        self.is_on = is_on
        if redraw:
            self.draw()

    def draw(self):
        self.delete("all")
        r = self.height / 2
        color = self.track_on if self.is_on else self.track_off

        self.create_oval(0, 0, self.height, self.height,
                          fill=color, outline=color)
        self.create_oval(self.width - self.height, 0, self.width,
                          self.height, fill=color, outline=color)
        self.create_rectangle(r, 0, self.width - r, self.height,
                               fill=color, outline=color)

        knob_d = self.height - 6
        x0 = (self.width - self.height + 3) if self.is_on else 3
        self.create_oval(x0, 3, x0 + knob_d, 3 + knob_d,
                          fill=self.knob_color, outline=self.knob_color)

    def _on_click(self, _event):
        self.is_on = not self.is_on
        self.draw()
        if self.command:
            self.command(self.is_on)


class AddDepartmentDialog(tk.Toplevel):
    """GUI window for adding a new department, with a light/dark toggle."""

    def __init__(self, parent, on_department_added=None, dark_mode=False):
        super().__init__(parent)

        self.parent = parent
        self.on_department_added = on_department_added

        self.dark_mode = dark_mode
        self.theme = DARK_THEME if dark_mode else LIGHT_THEME

        self.title("Add New Department")
        self.geometry("560x420")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        # Widgets we need to re-color on theme toggle live here.
        self._themed_widgets = []

        self.create_widgets()
        self.apply_theme()

    # =========================
    # HELPERS
    # =========================

    def _track(self, widget, kind):
        """Remember a widget + which theme keys it should get on toggle."""
        self._themed_widgets.append((widget, kind))
        return widget

    def _load_header_icon(self, label_widget):
        """Loads assets/department.png into the header badge. """
        if not PIL_AVAILABLE:
            label_widget.configure(text="\U0001F3E5", font=("Segoe UI", 16))
            return

        image_path = os.path.join(
            os.path.dirname(__file__), "assets", "department.png"
        )

        try:
            image = Image.open(image_path).convert("RGBA")

            # Center-crop to a square so the icon isn't stretched.
            w, h = image.size
            side = min(w, h)
            left = (w - side) // 2
            top = (h - side) // 2
            image = image.crop((left, top, left + side, top + side))

            # Resize to fill the badge nicely.
            icon_size = 40
            image = image.resize((icon_size, icon_size), Image.LANCZOS)

            self._header_icon_img = ImageTk.PhotoImage(image)
            label_widget.configure(image=self._header_icon_img, text="")
        except Exception:
            label_widget.configure(text="\U0001F3E5", font=("Segoe UI", 16))

    def _make_field(self, parent_frame, row, icon, label_text, placeholder):
        """Builds one 'icon + label' row plus its input box, returns the entry."""

        label_row = tk.Frame(parent_frame)
        label_row.grid(row=row * 2, column=0, sticky="w", padx=2,
                        pady=(0, 6))
        self._track(label_row, "body")

        icon_lbl = tk.Label(
            label_row, text=icon, font=("Segoe UI", 11),
        )
        icon_lbl.pack(side="left")
        self._track(icon_lbl, "accent_on_body")

        text_lbl = tk.Label(
            label_row, text=label_text, font=("Segoe UI", 10, "bold"),
        )
        text_lbl.pack(side="left", padx=(6, 0))
        self._track(text_lbl, "text_on_body")

        box = tk.Frame(parent_frame, highlightthickness=0, bd=0)
        box.grid(row=row * 2 + 1, column=0, sticky="ew", pady=(0, 16))
        self._track(box, "field_box")

        entry = tk.Entry(
            box, font=("Segoe UI", 10), bd=0, relief="flat",
            highlightthickness=0,
        )
        entry.pack(fill="both", expand=True, ipady=8, padx=10)
        self._track(entry, "field_text")

        self._add_placeholder(entry, placeholder)
        parent_frame.grid_columnconfigure(0, weight=1)
        return entry

    def _add_placeholder(self, widget, placeholder):
        """Light-gray placeholder text that clears on focus."""

        def show_placeholder():
            widget.delete(0, "end")
            widget.insert(0, placeholder)
            widget.configure(fg=self.theme["placeholder"])
            widget._showing_placeholder = True

        def on_focus_in(_event):
            if getattr(widget, "_showing_placeholder", False):
                widget.delete(0, "end")
                widget.configure(fg=self.theme["text"])
                widget._showing_placeholder = False

        def on_focus_out(_event):
            if not widget.get().strip():
                show_placeholder()

        widget._placeholder = placeholder
        widget.bind("<FocusIn>", on_focus_in)
        widget.bind("<FocusOut>", on_focus_out)
        show_placeholder()

    def _get_value(self, widget):
        """Returns '' if the field is still showing its placeholder."""
        if getattr(widget, "_showing_placeholder", False):
            return ""
        return widget.get().strip()

    # =========================
    # BUILD UI
    # =========================

    def create_widgets(self):

        outer = tk.Frame(self, highlightthickness=1)
        outer.pack(fill="both", expand=True, padx=14, pady=14)
        self._track(outer, "card")

        # ---------- Header ----------
        header = tk.Frame(outer)
        header.pack(fill="x", padx=22, pady=(20, 12))
        self._track(header, "body")

        icon_badge = tk.Frame(header, width=48, height=48)
        icon_badge.grid(row=0, column=0, rowspan=2, padx=(0, 12))
        icon_badge.grid_propagate(False)
        icon_badge.pack_propagate(False)
        self._track(icon_badge, "icon_badge_frame")

        icon_wrap = tk.Label(icon_badge)
        icon_wrap.pack(expand=True)
        self._load_header_icon(icon_wrap)
        self._track(icon_wrap, "icon_badge")

        title_lbl = tk.Label(
            header, text="Add New Department",
            font=("Segoe UI", 15, "bold"), anchor="w",
        )
        title_lbl.grid(row=0, column=1, sticky="w")
        self._track(title_lbl, "text_on_body")

        subtitle_lbl = tk.Label(
            header, text="Enter the department details below",
            font=("Segoe UI", 9), anchor="w",
        )
        subtitle_lbl.grid(row=1, column=1, sticky="w")
        self._track(subtitle_lbl, "subtitle_on_body")

        header.grid_columnconfigure(1, weight=1)

        # Theme toggle: icon + pill switch, like the sidebar control
        toggle_wrap = tk.Frame(header)
        toggle_wrap.grid(row=0, column=2, rowspan=2, padx=(8, 12))
        self._track(toggle_wrap, "body")

        self.toggle_icon = tk.Label(
            toggle_wrap, text=("\u2600" if self.dark_mode else "\u263D"),
            font=("Segoe UI", 11),
        )
        self.toggle_icon.pack(side="left", padx=(0, 6))
        self._track(self.toggle_icon, "accent_on_body")

        self.toggle_switch = ToggleSwitch(
            toggle_wrap, command=self._on_toggle_switch
        )
        self.toggle_switch.pack(side="left")
        self.toggle_switch.set_state(self.dark_mode, redraw=False)

        close_btn = tk.Button(
            header, text="\u2715", font=("Segoe UI", 11), bd=0,
            relief="flat", cursor="hand2", command=self.destroy, width=3,
        )
        close_btn.grid(row=0, column=3, rowspan=2)
        self._track(close_btn, "close_btn")

        # divider
        divider = tk.Frame(outer, height=1)
        divider.pack(fill="x", padx=0)
        self._track(divider, "divider")

        # ---------- Form ----------
        form = tk.Frame(outer)
        form.pack(fill="both", expand=True, padx=22, pady=18)
        self._track(form, "body")

        # Department Name, full width — the only field this dialog needs
        name_col = tk.Frame(form)
        name_col.pack(fill="x")
        self._track(name_col, "body")
        self.name_entry = self._make_field(
            name_col, 0, "\U0001F3E5", "Department Name",
            "e.g. Cardiology",
        )

        # ---------- Footer / Buttons ----------
        footer_divider = tk.Frame(outer, height=1)
        footer_divider.pack(fill="x")
        self._track(footer_divider, "divider")

        footer = tk.Frame(outer)
        footer.pack(fill="x", padx=22, pady=16)
        self._track(footer, "footer")

        self.cancel_button = tk.Button(
            footer, text="Cancel", command=self.destroy,
            font=("Segoe UI", 10, "bold"), bd=1, relief="solid",
            cursor="hand2", padx=18, pady=6,
        )
        self.cancel_button.pack(side="right", padx=(10, 0))
        self._track(self.cancel_button, "cancel_btn")

        self.add_button = tk.Button(
            footer, text="+  Add Department", command=self.add_department,
            font=("Segoe UI", 10, "bold"), bd=0, relief="flat",
            cursor="hand2", padx=18, pady=6,
        )
        self.add_button.pack(side="right")
        self._track(self.add_button, "accent_btn")

        self.name_entry.focus()

    # =========================
    # THEME
    # =========================

    def apply_theme(self):
        t = self.theme
        self.configure(bg=t["body_bg"])

        for widget, kind in self._themed_widgets:
            if kind == "card":
                widget.configure(bg=t["card_bg"],
                                  highlightbackground=t["border"],
                                  highlightcolor=t["border"])
            elif kind == "body":
                widget.configure(bg=t["body_bg"])
            elif kind == "footer":
                widget.configure(bg=t["footer_bg"])
            elif kind == "divider":
                widget.configure(bg=t["border"])
            elif kind == "text_on_body":
                widget.configure(bg=t["body_bg"], fg=t["text"])
            elif kind == "subtitle_on_body":
                widget.configure(bg=t["body_bg"], fg=t["subtitle"])
            elif kind == "accent_on_body":
                widget.configure(bg=t["body_bg"], fg=t["accent"])
            elif kind == "icon_badge_frame":
                widget.configure(bg=t["icon_bg"])
            elif kind == "icon_badge":
                widget.configure(bg=t["icon_bg"], fg=t["accent"])
            elif kind == "close_btn":
                widget.configure(bg=t["close_bg"], fg=t["close_fg"],
                                  activebackground=t["close_bg"],
                                  activeforeground=t["accent"])
            elif kind == "field_box":
                widget.configure(bg=t["field_bg"])
            elif kind == "field_text":
                fg = (t["placeholder"]
                      if getattr(widget, "_showing_placeholder", False)
                      else t["text"])
                widget.configure(bg=t["field_bg"], fg=fg,
                                  insertbackground=t["text"])
            elif kind == "cancel_btn":
                widget.configure(bg=t["cancel_bg"], fg=t["cancel_text"],
                                  highlightbackground=t["cancel_border"],
                                  activebackground=t["field_bg"],
                                  activeforeground=t["cancel_text"])
            elif kind == "accent_btn":
                widget.configure(bg=t["accent"], fg=t["accent_text"],
                                  activebackground=t["accent_hover"],
                                  activeforeground=t["accent_text"])

        self.toggle_switch.set_colors(
            track_on=t["switch_track_on"],
            track_off=t["switch_track_off"],
            knob_color=t["switch_knob"],
            bg=t["body_bg"],
        )

    def _on_toggle_switch(self, is_on):
        self.dark_mode = is_on
        self.theme = DARK_THEME if self.dark_mode else LIGHT_THEME
        self.toggle_icon.configure(
            text=("\u2600" if self.dark_mode else "\u263D")
        )
        self.apply_theme()

    # =========================
    # ADD DEPARTMENT
    # =========================

    def add_department(self):

        name = self._get_value(self.name_entry)

        # ---- Validation ----

        if not name:
            messagebox.showerror(
                "Invalid Input",
                "Please enter the department name.",
                parent=self,
            )
            self.name_entry.focus()
            return

        # ---- Create Department Object ----

        department = Department(name)

        # ---- Send to Main Window ----

        if self.on_department_added:
            self.on_department_added(department)

        # ---- Success Message ----

        messagebox.showinfo(
            "Success",
            f"Department added successfully!\n\n"
            f"Department: {department.name}",
            parent=self,
        )

        self.destroy()


# =========================
# TEST WINDOW
# =========================

if __name__ == "__main__":

    root = tk.Tk()
    root.title("Hospital OOP - Test")
    root.geometry("300x150")
    root.configure(bg="#FFFFFF")

    AddDepartmentDialog(root)

    root.mainloop()