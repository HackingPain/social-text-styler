# Social Text Styler

A single-file Python GUI tool that converts plain text into Unicode bold, italic, and underline characters for use on social media (Instagram, Facebook, X, LinkedIn, etc.).

## Features

- **Font families:** Serif and Sans-Serif
- **Styles:** Bold, Italic, Underline (independent toggles)
- **Live preview** as you type
- **Copy / Clear / Swap** controls
- Zero dependencies beyond Python's built-in `tkinter`

## Usage

```bash
python social_text_styler.py
```

Requires Python 3.10+ (uses `match`-style type hints). No pip install needed.

## How It Works

Maps ASCII A-Z, a-z, and 0-9 to their equivalents in the [Mathematical Alphanumeric Symbols](https://www.unicode.org/charts/PDF/U1D400.pdf) Unicode block. Underline uses the combining low line character (U+0332).

## License

Public domain. Do whatever you want with it.
