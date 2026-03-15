# Social Text Styler

Convert plain text into Unicode-styled text for social media - Instagram, Facebook, X, LinkedIn, and more.

## Web Version (index.html)

A single-file web app with no dependencies. Just open `index.html` in any browser.

### Features

- **19 Unicode styles** - Bold, Italic, Script, Fraktur, Double-Struck, Monospace, Circled, Squared, Fullwidth, Small Caps, Superscript, and more
- **Live preview grid** - type once, see all styles simultaneously
- **One-click copy** - click any style card to copy to clipboard
- **Stackable modifiers** - underline, strikethrough, and overline combine with any style
- **Favorites** - star frequently-used styles to pin them to the top (persisted in localStorage)
- **Dark theme** with glass-morphism design
- **Responsive** - works on desktop and mobile
- **Keyboard accessible** - Tab to navigate, Enter/Space to copy
- **Zero dependencies** - vanilla HTML/CSS/JS, works offline

### Usage

Open `index.html` in a browser, or serve it from any static host.

## Python Version (social_text_styler.py)

The original tkinter desktop GUI. Supports Serif/Sans-Serif with Bold, Italic, and Underline toggles.

```bash
python social_text_styler.py
```

Requires Python 3.10+.

## How It Works

Maps ASCII A-Z, a-z, and 0-9 to their equivalents in Unicode's [Mathematical Alphanumeric Symbols](https://www.unicode.org/charts/PDF/U1D400.pdf) block and other styled character ranges. Modifiers use combining characters (U+0332 underline, U+0336 strikethrough, U+0305 overline).

## License

Public domain. Do whatever you want with it.
