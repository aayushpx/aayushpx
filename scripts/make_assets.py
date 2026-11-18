import base64, io, math, sys
from fontTools import subset
from fontTools.ttLib import TTFont

F = {"Anton": "/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf",
     "Mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
     "MonoB": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
     "Sans": "/usr/share/fonts/opentype/inter/Inter-Regular.otf"}
THEMES = {
  "dark":  dict(BG="#0A0D12", GRID="#16202B", TXT="#EEF2F6", MUT="#6B7A8C", AMB="#FFB547", CYN="#4FD1E8", GRN="#59E38C",
                LINE="#1F2A36", LINE2="#2A3746", DASH="#223040", BODY="#C3CCD7"),
  "light": dict(BG="#FFFFFF", GRID="#EEF1F4", TXT="#11161C", MUT="#6A7684", AMB="#C2610C", CYN="#0B7A99", GRN="#1A7F37",
                LINE="#D9DFE6", LINE2="#C3CBD4", DASH="#D3DAE2", BODY="#3A4652"),
}
def set_theme(name):
    globals().update(THEMES[name])
set_theme("dark")

def face(n, chars):
    f = TTFont(F[n]); o = subset.Options(); s = subset.Subsetter(o); s.populate(text=chars + " "); s.subset(f)
    b = io.BytesIO(); f.save(b)
    return f"@font-face{{font-family:{n};src:url(data:font/ttf;base64,{base64.b64encode(b.getvalue()).decode()})}}"

class S:
    def __init__(s): s.used = {k: "" for k in F}; s.b = []
    def t(s, font, x, y, size, fill, txt, extra=""):
        s.used[font] += txt
        s.b.append(f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" {extra}>{txt.replace("&","&amp;")}</text>')
    def r(s, raw): s.b.append(raw)
    def out(s, w, h, title):
        css = "".join(face(n, u) for n, u in s.used.items() if u)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">'
                f'<title>{title}</title><style>{css}@keyframes bl{{0%,60%{{opacity:1}}61%,100%{{opacity:.15}}}}.blink{{animation:bl 1.4s infinite}}</style>'
                + "".join(s.b) + "</svg>")

def grid(s, w, h, step=32):
    s.r(f'<rect width="{w}" height="{h}" rx="14" fill="{BG}"/>')
    s.r(f'<pattern id="g" width="{step}" height="{step}" patternUnits="userSpaceOnUse"><path d="M{step} 0H0V{step}" fill="none" stroke="{GRID}" stroke-width="1"/></pattern>')
    s.r(f'<rect width="{w}" height="{h}" rx="14" fill="url(#g)" opacity=".55"/>')
    s.r(f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="{LINE}"/>')

def kepler_points(cx, cy, a, e, n=180):
    b = a * math.sqrt(1 - e * e); pts = []
    for i in range(n + 1):
        M = 2 * math.pi * i / n; E = M
        for _ in range(30): E -= (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
        # focus at origin offset: ellipse centre cx, perihelion on the LEFT (sun at left focus)
        x = cx - a * math.cos(E); y = cy - b * math.sin(E)
        pts.append((x, y))
    return pts, b

def header():
    W, H = 1280, 480; s = S(); grid(s, W, H)
    # HUD top
    s.t("MonoB", 40, 46, 15, AMB, "AAYUSHPX", 'letter-spacing="3"')
    s.t("Mono", 190, 46, 15, MUT, "//  SYS 01  //  NEW ZEALAND", 'letter-spacing="2"')
    s.r(f'<circle class="blink" cx="{W-150}" cy="41" r="5" fill="{GRN}"/>')
    s.t("MonoB", W - 40, 46, 15, GRN, "NOMINAL", 'letter-spacing="3" text-anchor="end"')
    s.r(f'<line x1="40" y1="64" x2="{W-40}" y2="64" stroke="{LINE}"/>')
    # name
    s.t("Anton", 36, 210, 128, TXT, "AAYUSH", 'letter-spacing="2"')
    s.t("Anton", 36, 352, 128, TXT, "PRAKASH", 'letter-spacing="2"')
    s.r(f'<rect x="40" y="383" width="56" height="4" fill="{AMB}"/>')
    s.t("Mono", 110, 390, 15, CYN, "SIMULATION / EMBEDDED / MACHINE LEARNING", 'letter-spacing="2.5"')
    # orbit
    cx, cy, a, e = 960, 218, 205, 0.76
    pts, b = kepler_points(cx, cy, a, e); fx = cx - a * e
    s.r(f'<ellipse cx="{cx}" cy="{cy}" rx="{a}" ry="{b:.1f}" fill="none" stroke="{LINE2}" stroke-width="1.5"/>')
    s.r(f'<line x1="{cx-a-20}" y1="{cy}" x2="{cx+a+20}" y2="{cy}" stroke="{DASH}" stroke-dasharray="3 6"/>')
    s.r(f'<circle cx="{fx:.1f}" cy="{cy}" r="16" fill="{AMB}" opacity=".12"/><circle cx="{fx:.1f}" cy="{cy}" r="8" fill="{AMB}"/>')
    xs = ";".join(f"{x:.1f}" for x, _ in pts); ys = ";".join(f"{y:.1f}" for _, y in pts)
    # radius vector (sweeps equal areas in equal times)
    s.r(f'<line x1="{fx:.1f}" y1="{cy}" x2="{pts[0][0]:.1f}" y2="{cy}" stroke="{CYN}" stroke-width="1" opacity=".45">'
        f'<animate attributeName="x2" dur="9s" repeatCount="indefinite" values="{xs}"/>'
        f'<animate attributeName="y2" dur="9s" repeatCount="indefinite" values="{ys}"/></line>')
    s.r(f'<circle r="13" fill="{CYN}" opacity=".18"><animate attributeName="cx" dur="9s" repeatCount="indefinite" values="{xs}"/><animate attributeName="cy" dur="9s" repeatCount="indefinite" values="{ys}"/></circle>')
    s.r(f'<circle r="6" fill="{CYN}"><animate attributeName="cx" dur="9s" repeatCount="indefinite" values="{xs}"/><animate attributeName="cy" dur="9s" repeatCount="indefinite" values="{ys}"/></circle>')
    s.t("Mono", cx - a - 4, cy + 26, 12, MUT, "PERIAPSIS", 'letter-spacing="2"')
    s.t("Mono", cx + a + 4, cy - 14, 12, MUT, "APHELION", 'letter-spacing="2" text-anchor="end"')
    s.t("Mono", cx, cy + b + 34, 12.5, MUT, f"e = {e:.2f}   ·   T = 9.0 s   ·   KEPLER II: EQUAL AREAS, EQUAL TIMES", 'text-anchor="middle" letter-spacing="1"')
    # bottom HUD
    s.r(f'<line x1="40" y1="{H-58}" x2="{W-40}" y2="{H-58}" stroke="{LINE}"/>')
    s.t("Mono", 40, H - 26, 14, MUT, "CS + DATA SCIENCE", 'letter-spacing="2.5"')
    s.t("MonoB", W - 40, H - 26, 14, AMB, "NASA SPACE APPS NZ   2ND '25   3RD '26", 'letter-spacing="2.5" text-anchor="end"')
    return s.out(W, H, "Aayush Prakash: simulation, embedded systems and machine learning")

def section(num, title, tags):
    W, H = 1280, 96; s = S(); grid(s, W, H, 24)
    s.t("MonoB", 36, 60, 18, AMB, f"{num:02d}", 'letter-spacing="2"')
    s.r(f'<line x1="78" y1="28" x2="78" y2="68" stroke="{LINE2}"/>')
    s.t("Anton", 98, 68, 46, TXT, title, 'letter-spacing="1.5"')
    s.t("Mono", W - 36, 58, 14, CYN, tags, 'letter-spacing="2" text-anchor="end"')
    return s.out(W, H, title)

def card(event, result, rcol, title, lines, role):
    W, H = 640, 280; s = S(); grid(s, W, H, 24)
    s.t("Mono", 28, 44, 15, MUT, event, 'letter-spacing="2"')
    s.t("Anton", W - 28, 104 if len(result) > 4 else 92, 54 if len(result) > 4 else 72, rcol, result, 'text-anchor="end" letter-spacing="1"')
    s.t("Anton", 26, 108, 44, TXT, title, 'letter-spacing="1"')
    for i, ln in enumerate(lines):
        s.t("Sans", 28, 156 + i * 31, 22, BODY, ln)
    s.r(f'<line x1="28" y1="{H-52}" x2="{W-28}" y2="{H-52}" stroke="{LINE}"/>')
    s.t("MonoB", 28, H - 22, 15, CYN, role, 'letter-spacing="2"')
    return s.out(W, H, f"{title}: {result}, {event}")

def wide(event, big, title, line, builds):
    W, H = 1280, 230; s = S(); grid(s, W, H, 24)
    s.t("Mono", 28, 44, 15, MUT, event, 'letter-spacing="2"')
    s.t("Anton", 26, 108, 44, TXT, title, 'letter-spacing="1"')
    s.t("Sans", 28, 148, 22, BODY, line)
    s.t("Anton", W - 28, 104, 72, AMB, big, 'text-anchor="end" letter-spacing="1"')
    s.r(f'<line x1="28" y1="{H-52}" x2="{W-28}" y2="{H-52}" stroke="{LINE}"/>')
    s.t("MonoB", 28, H - 22, 15, CYN, "   /   ".join(builds), 'letter-spacing="2"')
    return s.out(W, H, f"{title}: {big}")

def feature(img, event, place, title, lines, role):
    cur = dict((k, globals()[k]) for k in THEMES["dark"]); set_theme("dark")
    W, H = 1280, 420; s = S()
    b64 = base64.b64encode(open(img, "rb").read()).decode()
    s.r(f'<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath>'
        f'<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{BG}" stop-opacity=".94"/>'
        f'<stop offset=".42" stop-color="{BG}" stop-opacity=".78"/><stop offset=".7" stop-color="{BG}" stop-opacity="0"/></linearGradient></defs>')
    s.r(f'<g clip-path="url(#c)"><image width="{W}" height="{H}" href="data:image/jpeg;base64,{b64}"/><rect width="{W}" height="{H}" fill="url(#fade)"/></g>')
    s.r(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{LINE}"/>')
    s.t("Mono", 40, 54, 15, MUT, event, 'letter-spacing="2"')
    s.t("Anton", 38, 150, 84, TXT, title, 'letter-spacing="1.5"')
    s.t("Anton", 40, 224, 58, AMB, place, 'letter-spacing="2"')
    for i, ln in enumerate(lines):
        s.t("Sans", 40, 284 + i * 32, 23, "#D3DAE2", ln)
    s.t("MonoB", 40, H - 34, 15, CYN, role, 'letter-spacing="2"')
    out = s.out(W, H, f"{title}: {place}, {event}"); globals().update(cur); return out

def project_card(img, tag, title, sub, lines, chips, url_hint="VIEW REPO  →", iw=840, ih=420, ix=None, iy=0):
    cur = dict((k, globals()[k]) for k in THEMES["dark"]); set_theme("dark")
    W, H = 1280, 420; s = S()
    b64 = base64.b64encode(open(img, "rb").read()).decode()
    s.r(f'<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath>'
        f'<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{BG}"/><stop offset=".30" stop-color="{BG}"/>'
        f'<stop offset=".52" stop-color="{BG}" stop-opacity=".55"/><stop offset=".75" stop-color="{BG}" stop-opacity="0"/></linearGradient></defs>')
    s.r(f'<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{BG}"/><image x="{W-iw if ix is None else ix}" y="{iy}" width="{iw}" height="{ih}" href="data:image/jpeg;base64,{b64}"/><rect width="{W}" height="{H}" fill="url(#fade)"/></g>')
    s.r(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{LINE}"/>')
    s.t("Mono", 40, 54, 15, AMB, tag, 'letter-spacing="2"')
    s.t("Anton", 38, 150, 84, TXT, title, 'letter-spacing="1.5"')
    s.t("Mono", 42, 192, 16, CYN, sub, 'letter-spacing="2"')
    for i, ln in enumerate(lines):
        s.t("Sans", 40, 246 + i * 32, 23, "#D3DAE2", ln)
    s.t("MonoB", 40, H - 34, 15, MUT, chips, 'letter-spacing="2"')
    s.t("MonoB", W - 40, H - 34, 15, AMB, url_hint, 'letter-spacing="2" text-anchor="end"')
    out = s.out(W, H, title); globals().update(cur); return out

if __name__ == "__main__":
    o = sys.argv[1]
    for theme in ("dark", "light"):
      set_theme(theme); sfx = "-" + theme
      open(f"{o}/header{sfx}.svg", "w").write(header())
      for i, (slug, title, tags) in enumerate([
          ("projects", "PROJECTS", "EMBEDDED  ·  ESP32-S3  ·  C"),
          ("hackathons", "HACKATHONS", "2ND '25  ·  3RD '26"),
          ("bench", "THE BENCH", "C++  ·  PYTHON  ·  R"),
          ("telemetry", "TELEMETRY", "LIVE  ·  UPDATED DAILY"),
          ("toolkit", "TOOLKIT", "")], 1):
          open(f"{o}/s{i}-{slug}{sfx}.svg", "w").write(section(i, title, tags))
      open(f"{o}/p-launcher.svg", "w").write(project_card("scripts/src/launcher_card.jpg", "HARDWARE  ·  2026", "LAUNCHER",
          "MISSION CONTROL ON A T-DISPLAY S3",
          ["A launch-sequence state machine, live IMU", "telemetry over MQTT, and a mission event log,", "all in C on bare ESP-IDF."],
          "ESP32-S3  ·  C  ·  MPU6050  ·  MQTT"))
      open(f"{o}/p-neo.svg", "w").write(project_card("scripts/src/neo_card.jpg", "GAME  ·  2026", "NEO",
          "A MATRIX DODGE GAME FOR THE T-DISPLAY S3",
          ["Dodge bullets that keep getting faster.", "Procedural Matrix rain, a ramping difficulty", "curve and a high score saved to flash."],
          "ESP32-S3  ·  C  ·  NVS  ·  GAME LOOP", iw=559, ih=330, ix=660, iy=26))
      open(f"{o}/hk-spherex.svg", "w").write(feature("scripts/src/spherex_bg.jpg", "NASA SPACE APPS NZ  ·  2026  ·  PLANET X AND SPHEREX CHALLENGE", "3RD PLACE", "SPHEREXPLORER",
          ["Real SPHEREx survey data, pulled live from IRSA", "into a cinematic, explorable sky."], "PROJECT LEAD  ·  REMOTE TECH LEAD  ·  BACKEND + DATA"))
      open(f"{o}/hk-exoplanet{sfx}.svg", "w").write(card("NASA SPACE APPS NZ  ·  2025", "2ND", AMB, "EXOPLANET EXPLORER",
          ["An ML pipeline that turns telescope data", "into 3D habitability visualisations."], "TEAM LEAD  ·  ML PIPELINE"))
      open(f"{o}/hk-orbitguard{sfx}.svg", "w").write(card("ACTINSPACE NZ  ·  2026", "24H", CYN, "ORBITGUARD",
          ["A skip-connection LSTM that models how", "satellite collision risk evolves over time."], "TEAM LEAD  ·  SYSTEM DESIGN + PITCH"))
      open(f"{o}/hk-midnight{sfx}.svg", "w").write(card("MIDNIGHT HACKATHON  ·  2026", "ZK", CYN, "MIDNIGHT HR",
          ["Proves a salary fits the approved budget", "without ever revealing the salary."], "TEAM LEAD  ·  PRIVACY ARCHITECTURE"))
      open(f"{o}/hk-mlh-card{sfx}.svg", "w").write(card("MLH GLOBAL HACK WEEK  ·  2026", "6 BUILDS", AMB, "AGENTS WEEK",
          ["Every challenge, six agent builds,", "two all-nighters."], "FORGE  ·  TERMGEN  ·  ORBITOPS  ·  +3"))
      open(f"{o}/hk-mlh{sfx}.svg", "w").write(wide("MLH GLOBAL HACK WEEK: AGENTS  ·  2026", "6 BUILDS", "ONE WEEK, EVERY CHALLENGE",
          "Two all-nighters, six agent projects: multi-agent pipelines, terminal tools and a mission-ops sim.",
          ["FORGE", "TERMGEN", "ORBITOPS", "REPOLENS", "AGENT-MEMORY", "COMMIT SAGE"]))
      print("ok")
