"""Render Inner Moon carousel slides from the brand tokens + a content JSON.

Usage:  python3 render.py <content.json> <out_dir>
content.json = {"date": "2026-10-13", "slides": [{"template": "hook", ...fields}, ...]}
Fails (exit 1) if any field is over its character limit or any slide's text runs into the bottom safe zone.
"""
import base64, html, json, pathlib, random, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
BRAND = HERE.parent / "brand"
TOK = json.loads((BRAND / "tokens.json").read_text())
C = {k: v["hex"] for k, v in TOK["color"].items()}
W, H, SAFE = TOK["canvas"]["width"], TOK["canvas"]["height"], TOK["canvas"]["safe_bottom"]
LIM = TOK["limits_chars"]

GLYPHS = dict(Aries="♈", Taurus="♉", Gemini="♊", Cancer="♋", Leo="♌", Virgo="♍",
              Libra="♎", Scorpio="♏", Sagittarius="♐", Capricorn="♑", Aquarius="♒", Pisces="♓")
DATES = dict(Aries="Mar 21 – Apr 19", Taurus="Apr 20 – May 20", Gemini="May 21 – Jun 20", Cancer="Jun 21 – Jul 22",
             Leo="Jul 23 – Aug 22", Virgo="Aug 23 – Sep 22", Libra="Sep 23 – Oct 22", Scorpio="Oct 23 – Nov 21",
             Sagittarius="Nov 22 – Dec 21", Capricorn="Dec 22 – Jan 19", Aquarius="Jan 20 – Feb 18", Pisces="Feb 19 – Mar 20")
LIMIT_MAP = {"hook": {"kicker": "kicker", "headline": "hook_headline", "sub": "hook_sub"},
             "sign": {"body": "sign_body", "question": "sign_question"},
             "cta": {"headline": "cta_headline", "sub": "cta_sub"}}

def b64(p, mime): return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()

def font_faces():
    t = TOK["type"]; f = lambda i: (BRAND / t["serif"]["files"][i]).as_uri()
    return (f"@font-face{{font-family:Schola;src:url({f(0)})}}"
            f"@font-face{{font-family:Schola;font-style:italic;src:url({f(1)})}}"
            f"@font-face{{font-family:Schola;font-weight:700;src:url({f(2)})}}"
            f"@font-face{{font-family:Schola;font-weight:700;font-style:italic;src:url({f(3)})}}"
            f"@font-face{{font-family:IMGlyph;src:url({(BRAND / t['glyph']['files'][0]).as_uri()})}}")

def sky(seed):
    r = random.Random(seed)
    dots = "".join(f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(0,H):.0f}" r="{r.choice([.8,1,1.2,1.6,2.2])}" fill="{C["gold"]}" opacity="{r.uniform(.3,.9):.2f}"/>' for _ in range(380))
    spk = "".join(f'<g transform="translate({r.uniform(100,980):.0f} {y}) scale({r.uniform(.25,.45):.2f})"><path d="M0 -50C3 -12 12 -3 50 0C12 3 3 12 0 50C-3 12 -12 3 -50 0C-12 -3 -3 -12 0 -50Z" fill="#F3DCA0"/></g>' for y in (1150, 1190, 1240))
    n1, n2 = (r.uniform(700, 950), r.uniform(650, 950)), (r.uniform(100, 300), r.uniform(200, 400))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><defs><radialGradient id="n"><stop offset="0" stop-color="{C["nebula"]}" stop-opacity=".5"/>'
           f'<stop offset="1" stop-color="{C["nebula"]}" stop-opacity="0"/></radialGradient></defs><rect width="{W}" height="{H}" fill="{C["void"]}"/>'
           f'<ellipse cx="{n1[0]:.0f}" cy="{n1[1]:.0f}" rx="420" ry="300" fill="url(#n)"/><ellipse cx="{n2[0]:.0f}" cy="{n2[1]:.0f}" rx="380" ry="240" fill="url(#n)" opacity=".55"/>{dots}{spk}</svg>')
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()

STAR = lambda s: f'<svg width="{s}" height="{s}" viewBox="0 0 100 100"><path d="M50 0C53 38 62 47 100 50C62 53 53 62 50 100C47 62 38 53 0 50C38 47 47 38 50 0Z" fill="{C["cream"]}"/></svg>'

def css(bg):
    m = TOK["mascot"]["sizes"]; s = TOK["type"]["scale"]
    return f"""{font_faces()}
*{{box-sizing:border-box}}
:root{{--void:{C['void']};--cream:{C['cream']};--gold:{C['gold']};--blush:{C['blush']};--moon-hook:{m['hook']}px;--moon-corner:{m['sign_corner']}px;--moon-cta:{m['cta']}px}}
body{{margin:0;width:{W}px;height:{H}px;position:relative;overflow:hidden;background:var(--void) url('{bg}') center/cover;color:var(--cream);font-family:Schola,serif}}
.frame{{position:absolute;inset:40px;border:3px solid var(--cream);outline:1px solid var(--cream);outline-offset:-14px;opacity:.85}}
#content{{position:absolute}} .center{{left:110px;right:110px;text-align:center}}
.kicker{{font-size:{s['kicker']['size']}px;letter-spacing:{s['kicker']['tracking']};text-transform:uppercase;color:var(--blush)}}
.headline{{font-weight:700;font-size:{s['headline']['size']}px;line-height:{s['headline']['line']};margin:0}}
.sub{{font-style:italic;font-size:{s['sub']['size']}px;margin-top:30px;color:var(--blush)}}
.rule{{display:flex;align-items:center;gap:18px;margin:34px 0}}
.rule:before,.rule:after{{content:"";flex:1;height:2px;background:var(--cream);opacity:.8}}
.moon{{filter:{TOK['mascot']['glow']}}}
.signrow{{display:flex;align-items:baseline;gap:30px;margin-top:40px}}
.glyph{{font-family:IMGlyph;font-size:116px;color:var(--blush)}}
.signname{{font-size:{s['sign_name']['size']}px;font-weight:700;margin:0;line-height:1}}
.dates{{font-style:italic;font-size:30px;color:var(--gold);margin-top:8px}}
.body{{font-size:{s['body']['size']}px;line-height:{s['body']['line']};margin:0;color:var(--gold)}}
.ask{{margin-top:60px;border-left:6px solid var(--blush);padding-left:34px}}
.question{{font-style:italic;font-size:{s['question']['size']}px;line-height:{s['question']['line']};margin:14px 0 0}}
"""

def fill(template, fields):
    out = (HERE / f"slide-{template}.html").read_text()
    for k, v in fields.items():
        out = out.replace("{{" + k + "}}", v if k in ("moon", "star", "glyph") else html.escape(str(v)))
    return out

def check_limits(i, s):
    errs = []
    for field, key in LIMIT_MAP.get(s["template"], {}).items():
        if len(s.get(field, "")) > LIM[key]:
            errs.append(f"slide {i}: {field} is {len(s[field])} chars (limit {LIM[key]})")
    return errs

def main(content_path, out_dir):
    data = json.loads(pathlib.Path(content_path).read_text())
    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    moon = b64(BRAND / TOK["mascot"]["file"], "image/png")
    errors, signs = [], [s for s in data["slides"] if s["template"] == "sign"]
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        for i, s in enumerate(data["slides"], 1):
            errors += check_limits(i, s)
            f = dict(s, moon=moon, star=STAR(34 if s["template"] == "hook" else 30), handle=s.get("handle", "@innermoonstore"))
            if s["template"] == "sign":
                f.update(glyph=GLYPHS[s["sign"]] + "︎", dates=DATES[s["sign"]], count=str(len(signs)), index=str(signs.index(s) + 1),
                         signsize=str(150 if len(s["sign"]) <= 6 else 150 if len(s["sign"]) <= 7 else int(150 * 7 / len(s["sign"]))))
            pg.set_content(f"<html><head><style>{css(sky(data['date'] + str(i)))}</style></head><body>{fill(s['template'], f)}</body></html>")
            pg.wait_for_timeout(250)
            # shrink long sign names until they clear the corner moon
            pg.evaluate("""() => { const n = document.querySelector('.signname'); if (!n) return;
              const limit = document.querySelector('.moon').getBoundingClientRect().left - 30; let s = parseFloat(getComputedStyle(n).fontSize);
              while (n.getBoundingClientRect().right > limit && s > 70) { s -= 4; n.style.fontSize = s + 'px'; } }""")
            if pg.evaluate("document.querySelector('.kicker').getBoundingClientRect().height") > 40:
                errors.append(f"slide {i}: kicker wraps to two lines")
            bottom = pg.evaluate("document.getElementById('content').getBoundingClientRect().bottom")
            if bottom > SAFE:
                errors.append(f"slide {i}: text ends at {bottom:.0f}px, past the safe zone ({SAFE}px)")
            pg.screenshot(path=str(out / f"slide-{i}.jpg"), type="jpeg", quality=90)
        b.close()
    for e in errors: print("QA FAIL:", e)
    print(f"rendered {len(data['slides'])} slides to {out}" + ("" if errors else " · QA passed"))
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
