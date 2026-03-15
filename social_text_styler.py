#!/usr/bin/env python3
"""
Social Text Styler - a tiny GUI to generate bold/italic/underline Unicode text for social media.

Features
- Family: Serif or Sans‑Serif
- Weight/Style: Bold, Italic (independent toggles)
- Underline: adds combining underline to each non‑space char
- Live preview as you type
- Copy output / Clear / Swap (send output back to input)
- Single‑file, zero dependencies (tkinter only)

Notes
- Many platforms (IG, FB, X, LinkedIn, etc.) support these Unicode “styled” letters.
- Underline uses the COMBINING LOW LINE (U+0332). Some apps render it imperfectly.
- Digits don’t have italic forms in the Mathematical Alphanumeric Symbols block; we fall back intelligently.

(c) 2025 Dom + ChatGPT. Do anything you want with it.
"""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox

COMBINING_UNDERLINE = "\u0332"

# --- Unicode mapping helpers -------------------------------------------------
# Mathematical Alphanumeric Symbols code points
# Ref: https://www.unicode.org/charts/PDF/U1D400.pdf

# Serif
SERIF_BOLD_UC = 0x1D400  # A-Z
SERIF_BOLD_LC = 0x1D41A  # a-z
SERIF_ITALIC_UC = 0x1D434
SERIF_ITALIC_LC = 0x1D44E
SERIF_BOLD_ITALIC_UC = 0x1D468
SERIF_BOLD_ITALIC_LC = 0x1D482

# Sans-Serif
SANS_UC = 0x1D5A0
SANS_LC = 0x1D5BA
SANS_BOLD_UC = 0x1D5D4
SANS_BOLD_LC = 0x1D5EE
SANS_ITALIC_UC = 0x1D608
SANS_ITALIC_LC = 0x1D622
SANS_BOLD_ITALIC_UC = 0x1D63C
SANS_BOLD_ITALIC_LC = 0x1D656

# Digits
DIGIT_BOLD = 0x1D7CE
DIGIT_SANS = 0x1D7E2
DIGIT_SANS_BOLD = 0x1D7EC

A_ORD = ord('A')
Z_ORD = ord('Z')
a_ORD = ord('a')
z_ORD = ord('z')
ZERO_ORD = ord('0')
NINE_ORD = ord('9')

StyleKey = tuple[str, bool, bool]  # (family, bold, italic)


def _alpha_map(start_uc: int, start_lc: int) -> dict[str, str]:
    """Build A-Z and a-z mapping starting at the given Unicode blocks."""
    m: dict[str, str] = {}
    for i in range(26):
        m[chr(A_ORD + i)] = chr(start_uc + i)
        m[chr(a_ORD + i)] = chr(start_lc + i)
    return m


def _digit_map(start_digit: int) -> dict[str, str]:
    m: dict[str, str] = {}
    for i in range(10):
        m[chr(ZERO_ORD + i)] = chr(start_digit + i)
    return m

# Precompute maps per style key
STYLE_MAPS: dict[StyleKey, dict[str, str]] = {}

# Serif family
STYLE_MAPS[("serif", False, False)] = {}  # plain serif == pass-through
STYLE_MAPS[("serif", True, False)] = _alpha_map(SERIF_BOLD_UC, SERIF_BOLD_LC) | _digit_map(DIGIT_BOLD)
STYLE_MAPS[("serif", False, True)] = _alpha_map(SERIF_ITALIC_UC, SERIF_ITALIC_LC)  # digits: no italic
STYLE_MAPS[("serif", True, True)] = _alpha_map(SERIF_BOLD_ITALIC_UC, SERIF_BOLD_ITALIC_LC) | _digit_map(DIGIT_BOLD)

# Sans family
STYLE_MAPS[("sans", False, False)] = _alpha_map(SANS_UC, SANS_LC) | _digit_map(DIGIT_SANS)
STYLE_MAPS[("sans", True, False)] = _alpha_map(SANS_BOLD_UC, SANS_BOLD_LC) | _digit_map(DIGIT_SANS_BOLD)
STYLE_MAPS[("sans", False, True)] = _alpha_map(SANS_ITALIC_UC, SANS_ITALIC_LC) | _digit_map(DIGIT_SANS)
STYLE_MAPS[("sans", True, True)] = _alpha_map(SANS_BOLD_ITALIC_UC, SANS_BOLD_ITALIC_LC) | _digit_map(DIGIT_SANS_BOLD)


def stylize(text: str, family: str = "serif", bold: bool = False, italic: bool = False, underline: bool = False) -> str:
    """Convert plain ASCII letters/digits to fancy Unicode per requested style.

    - family: "serif" or "sans"
    - bold, italic: independent toggles
    - underline: adds combining underline to each non-space character
    """
    key: StyleKey = (family, bool(bold), bool(italic))
    m = STYLE_MAPS.get(key, {})

    out_chars: list[str] = []
    for ch in text:
        # swap if mapped; otherwise pass-through
        mapped = m.get(ch, ch)
        if underline and not ch.isspace():
            mapped = mapped + COMBINING_UNDERLINE
        out_chars.append(mapped)
    return "".join(out_chars)


# --- GUI ---------------------------------------------------------------------
class App(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master, padding=16)
        self.master.title("Social Text Styler ✨")
        self.master.geometry("820x560")
        self.master.minsize(720, 520)
        try:
            self.master.iconbitmap('')  # harmless no-op on most platforms
        except Exception:
            pass

        self.family = tk.StringVar(value="sans")  # 'serif' or 'sans'
        self.bold = tk.BooleanVar(value=True)
        self.italic = tk.BooleanVar(value=False)
        self.underline = tk.BooleanVar(value=False)

        self._build()
        self._bind_events()
        self._update_output()

    def _build(self):
        # Style
        style = ttk.Style()
        # Use a simple, rounded theme if available
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        style.configure('TFrame', background='#101419')
        style.configure('TLabel', background='#101419', foreground='#E8EAED')
        style.configure('TCheckbutton', background='#101419', foreground='#E8EAED')
        style.configure('TRadiobutton', background='#101419', foreground='#E8EAED')
        style.configure('TButton', padding=(10, 6))
        style.map('TButton', background=[('active', '#1f2937')])

        # Header
        header = ttk.Frame(self)
        header.pack(fill='x', pady=(0, 12))
        ttk.Label(header, text='Social Text Styler', font=('Segoe UI', 18, 'bold')).pack(side='left')
        ttk.Label(header, text='  -  make your posts pop', font=('Segoe UI', 10)).pack(side='left')

        # Controls row
        controls = ttk.Frame(self)
        controls.pack(fill='x', pady=(0, 10))

        fam_box = ttk.LabelFrame(controls, text='Font Family')
        fam_box.pack(side='left', padx=(0, 12))
        ttk.Radiobutton(fam_box, text='Sans‑Serif', value='sans', variable=self.family).grid(row=0, column=0, sticky='w', padx=8, pady=6)
        ttk.Radiobutton(fam_box, text='Serif', value='serif', variable=self.family).grid(row=1, column=0, sticky='w', padx=8, pady=6)

        style_box = ttk.LabelFrame(controls, text='Style')
        style_box.pack(side='left', padx=(0, 12))
        ttk.Checkbutton(style_box, text='Bold', variable=self.bold).grid(row=0, column=0, sticky='w', padx=8, pady=6)
        ttk.Checkbutton(style_box, text='Italic', variable=self.italic).grid(row=0, column=1, sticky='w', padx=8, pady=6)
        ttk.Checkbutton(style_box, text='Underline', variable=self.underline).grid(row=0, column=2, sticky='w', padx=8, pady=6)

        btn_box = ttk.Frame(controls)
        btn_box.pack(side='left', padx=(0, 12))
        ttk.Button(btn_box, text='Copy Output', command=self.copy_output).grid(row=0, column=0, padx=6, pady=6)
        ttk.Button(btn_box, text='Clear', command=self.clear_all).grid(row=0, column=1, padx=6, pady=6)
        ttk.Button(btn_box, text='Swap ⟲', command=self.swap_texts).grid(row=0, column=2, padx=6, pady=6)

        # Text areas
        panes = ttk.Panedwindow(self, orient='horizontal')
        panes.pack(fill='both', expand=True)

        left = ttk.Labelframe(panes, text='Input')
        right = ttk.Labelframe(panes, text='Output (generated)')
        panes.add(left, weight=1)
        panes.add(right, weight=1)

        self.input = tk.Text(left, wrap='word', undo=True, font=('Segoe UI', 12))
        self.input.pack(fill='both', expand=True, padx=8, pady=8)
        self.input.insert('1.0', 'Type here…')
        self.input.tag_add('placeholder', '1.0', 'end')
        self.input.bind('<FocusIn>', self._clear_placeholder)

        self.output = tk.Text(right, wrap='word', undo=False, font=('Segoe UI', 12))
        self.output.pack(fill='both', expand=True, padx=8, pady=8)
        self.output.configure(state='disabled')

        # Status bar
        status = ttk.Frame(self)
        status.pack(fill='x', pady=(10, 0))
        self.status_lbl = ttk.Label(status, text='Ready')
        self.status_lbl.pack(side='left')

        self.pack(fill='both', expand=True)

    def _bind_events(self):
        for v in (self.family, self.bold, self.italic, self.underline):
            v.trace_add('write', lambda *_: self._update_output())
        self.input.bind('<<Modified>>', self._on_input_modified)

    # --- Event handlers ------------------------------------------------------
    def _clear_placeholder(self, _):
        if 'placeholder' in self.input.tag_names('1.0'):
            self.input.delete('1.0', 'end')
            self.input.tag_remove('placeholder', '1.0', 'end')

    def _on_input_modified(self, _):
        # Reset the modified flag and update output
        self.input.edit_modified(0)
        self._update_output()

    def _update_output(self):
        src = self.input.get('1.0', 'end-1c')
        out = stylize(
            src,
            family=self.family.get(),
            bold=self.bold.get(),
            italic=self.italic.get(),
            underline=self.underline.get(),
        )
        self.output.configure(state='normal')
        self.output.delete('1.0', 'end')
        self.output.insert('1.0', out)
        self.output.configure(state='disabled')
        self.status_lbl.config(text=f"Chars: {len(src)}  →  {len(out)} (underline adds combining marks)")

    def copy_output(self):
        data = self.output.get('1.0', 'end-1c')
        if not data:
            messagebox.showinfo('Copy Output', 'Nothing to copy yet.')
            return
        self.master.clipboard_clear()
        self.master.clipboard_append(data)
        self.status_lbl.config(text='Output copied to clipboard ✅')

    def clear_all(self):
        self.input.delete('1.0', 'end')
        self.output.configure(state='normal')
        self.output.delete('1.0', 'end')
        self.output.configure(state='disabled')
        self.status_lbl.config(text='Cleared')

    def swap_texts(self):
        out = self.output.get('1.0', 'end-1c')
        self.input.delete('1.0', 'end')
        self.input.insert('1.0', out)
        self._update_output()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
