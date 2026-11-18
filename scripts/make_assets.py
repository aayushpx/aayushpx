"""Generate typeset SVG assets (header, section titles, footer) for the profile README.
Fonts are subset and embedded as base64 so they render anywhere GitHub shows the image."""
import base64, io, sys
from fontTools import subset
from fontTools.ttLib import TTFont

LM = "/usr/share/texmf/fonts/opentype/public/lm/"
FONTS = {
    "Display": LM + "lmroman17-regular.otf",
    "Italic": LM + "lmroman12-italic.otf",
    "Mono": LM + "lmmono10-regular.otf",
    "MonoLt": LM + "lmmonolt10-regular.otf",
}
PAD = 6
THEMES = {
    "dark":  dict(text="#E6EDF3", muted="#8B949E", faint="#3D444D", accent="#F0A35E"),
    "light": dict(text="#1F2328", muted="#59636E", faint="#D1D9E0", accent="#B4541A"),
}

def font_face(name, path, chars):
    opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["kern", "liga"]
    try:
        f = TTFont(path); s = subset.Subsetter(opts); s.populate(text=chars); s.subset(f)
        buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf); fmt = "woff2"
    except Exception:
        opts.flavor = None; f = TTFont(path); s = subset.Subsetter(opts); s.populate(text=chars); s.subset(f)
        buf = io.BytesIO(); f.flavor = None; f.save(buf); fmt = "opentype"
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"@font-face{{font-family:'{name}';src:url(data:font/{fmt};base64,{b64}) format('{fmt}');}}"

def text_width(font, s, size, spacing=0):
    f = TTFont(FONTS[font]); cmap = f.getBestCmap(); hmtx = f["hmtx"]; upm = f["head"].unitsPerEm
    return sum(hmtx[cmap[ord(ch)]][0] for ch in s if ord(ch) in cmap) * size / upm + spacing * len(s)

def esc(t): return t.replace("&", "&amp;").replace("<", "&lt;")

def svg(w, h, body, texts, title):
    """texts: dict fontname -> all characters used with that font"""
    faces = "".join(font_face(n, FONTS[n], t + " ") for n, t in texts.items() if t)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
            f'<style>{faces}.d{{font-family:Display}}.i{{font-family:Italic}}.m{{font-family:Mono}}.ml{{font-family:MonoLt}}</style>'
            f'{body}</svg>')

class T:
    """Collects text per font so subsets contain exactly the glyphs used."""
    def __init__(self): self.used = {k: "" for k in FONTS}
    def __call__(self, font, cls, x, y, size, fill, s, extra=""):
        self.used[font] += s
        return f'<text class="{cls}" x="{x}" y="{y}" font-size="{size}" fill="{fill}" {extra}>{esc(s)}</text>'

def header(c):
    t = T(); W, H = 1280, 400
    b = []
    # top metadata line
    b.append(t("Mono", "m", PAD, 56, 16, c["accent"], "PROFILE  /  AAYUSHPX", 'letter-spacing="3"'))
    b.append(t("Mono", "m", W - PAD, 56, 16, c["muted"], "VOL. 2026  ·  REV. NOV", 'letter-spacing="3" text-anchor="end"'))
    b.append(f'<line x1="PAD" y1="74" x2="{W-PAD}" y2="74" stroke="{c["faint"]}" stroke-width="1"/>')
    # name + tagline
    b.append(t("Display", "d", PAD - 4, 196, 104, c["text"], "Aayush Prakash", 'letter-spacing="-1.5"'))
    b.append(t("Italic", "i", PAD, 248, 29, c["muted"], "Simulation, embedded systems & machine learning,"))
    b.append(t("Italic", "i", PAD, 284, 29, c["muted"], "built from first principles."))
    # orbit diagram (right)
    cx, cy, a, bb = 1010, 172, 146, 84
    e = (1 - (bb / a) ** 2) ** 0.5; fx = cx - a * e      # focus (sun) on the left
    apo = cx + a                                          # aphelion: far right
    b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{a}" ry="{bb}" fill="none" stroke="{c["muted"]}" stroke-width="1.2"/>')
    b.append(f'<line x1="{cx-a-18}" y1="{cy}" x2="{apo+18}" y2="{cy}" stroke="{c["faint"]}" stroke-width="1" stroke-dasharray="3 5"/>')
    b.append(f'<circle cx="{fx:.1f}" cy="{cy}" r="7" fill="{c["text"]}"/>')
    b.append(f'<circle cx="{apo}" cy="{cy}" r="5.5" fill="{c["accent"]}"/>')
    b.append(f'<circle cx="{apo}" cy="{cy}" r="12" fill="none" stroke="{c["accent"]}" stroke-width="1" opacity="0.6"/>')
    b.append(t("Mono", "m", apo - 6, cy - 22, 14, c["accent"], "APHELION", 'letter-spacing="2" text-anchor="end"'))
    b.append(t("Mono", "m", cx - a + 16, cy + 28, 14, c["muted"], "PERIAPSIS", 'letter-spacing="2"'))
    b.append(t("Italic", "i", cx, cy + bb + 40, 21, c["muted"],
               "r = a(1 − e²) / (1 + e cos f)", 'text-anchor="middle"'))
    # bottom row
    b.append(f'<line x1="PAD" y1="336" x2="{W-PAD}" y2="336" stroke="{c["faint"]}" stroke-width="1"/>')
    row = [("COMPUTER SCIENCE + DATA SCIENCE", c["muted"]), ("NEW ZEALAND", c["muted"]),
           ("NASA SPACE APPS NZ  ·  2ND ’25  ·  3RD ’26", c["accent"])]
    xs = [PAD, 560, W - PAD]; anchors = ["start", "start", "end"]
    for (s, col), x, an in zip(row, xs, anchors):
        b.append(t("Mono", "m", x, 370, 16, col, s, f'letter-spacing="2.5" text-anchor="{an}"'))
    return svg(W, H, "".join(b), t.used, "Aayush Prakash — simulation, embedded systems and machine learning, built from first principles")

def section(c, num, title):
    t = T(); W, H = 1280, 84
    b = [t("Mono", "m", PAD, 56, 17, c["accent"], f"§ {num:02d}", 'letter-spacing="2"'),
         t("Display", "d", PAD + 76, 58, 40, c["text"], title)]
    # hairline after the title: estimate title width (~0.48em per char for LM Roman)
    end = PAD + 76 + text_width("Display", title, 40) + 24
    b.append(f'<line x1="{end}" y1="46" x2="{W-PAD}" y2="46" stroke="{c["faint"]}" stroke-width="1"/>')
    return svg(W, H, "".join(b), t.used, title)

def footer(c):
    t = T(); W, H = 1280, 90
    b = [f'<line x1="PAD" y1="30" x2="{W-PAD}" y2="30" stroke="{c["faint"]}" stroke-width="1"/>',
         t("Mono", "m", W / 2, 66, 15, c["muted"], "—  END OF TRANSMISSION  —", 'letter-spacing="3" text-anchor="middle"')]
    return svg(W, H, "".join(b), t.used, "End of transmission")

SECTIONS = [("now", "Now"), ("feed", "Live feed"), ("flagship", "Flagship"),
            ("hackathons", "Hackathons"), ("scratch", "Built from scratch"),
            ("tools", "Tools & libraries"), ("toolkit", "Toolkit")]

if __name__ == "__main__":
    out = sys.argv[1]
    import os; os.makedirs(out, exist_ok=True)
    for theme, c in THEMES.items():
        open(f"{out}/header-{theme}.svg", "w").write(header(c))
        open(f"{out}/footer-{theme}.svg", "w").write(footer(c))
        for i, (slug, title) in enumerate(SECTIONS, 1):
            open(f"{out}/s{i:02d}-{slug}-{theme}.svg", "w").write(section(c, i, title))
    print("ok")
