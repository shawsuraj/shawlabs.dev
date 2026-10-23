"""Builds shawlabs.dev into dist/ (Vercel) and preview/ (Claude preview).
Pages live in src/pages; the first line of each is JSON metadata.
{{EXPLORER}} and {{CHART}} are replaced with src/explorer.html and chart.svg."""
import json, os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
CSS = open(os.path.join(SRC, "styles.css")).read()
EXPLORER_HTML = open(os.path.join(SRC, "explorer.html")).read()
EXPLORER_JS = open(os.path.join(SRC, "explorer.js")).read()
BENCH_JS = open(os.path.join(SRC, "bench.js")).read() + "\n" + open(os.path.join(SRC, "lab.js")).read()
SHELF = json.load(open(os.path.join(SRC, "shelf.json")))
CHART = open(os.path.join(ROOT, "chart.svg")).read()
HOST = "https://www.shawlabs.dev"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700;12..96,800'
         '&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=JetBrains+Mono:wght@400;500&display=swap">')
ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23121418'/%3E"
        "%3Ccircle cx='32' cy='32' r='11' fill='%23d93a40'/%3E%3C/svg%3E")
def shelf_html():
    out = []
    for e in SHELF:
        img = f'<img src="{e["img"]}" alt="" width="600" height="90" loading="lazy">' if e.get("img") else ""
        out.append(f'<a class="el" href="{e["url"]}"><span class="n">{e["year"]}</span><b>{e["sym"]}</b>'
                   f'<span class="nm">{e["name"]}</span><span class="k">{e["kind"]}</span>{img}<p>{e["line"]}</p></a>')
    out.append('<div class="el next"><span class="n">soon</span><b>?</b><span class="nm">Next element</span>'
               '<p>Whatever I build next lands on the scale or on this shelf.</p></div>')
    return "\n".join(out)

PAGES = ["index", "world-chaos-map", "building-in-public"]

def nav(cur):
    items = [("index.html", "Lab", cur == "index"), ("index.html#writing", "Writing", cur == "writing"),
             ("https://www.shawsuraj.com", "About me", False)]
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if c else ""}>{t}</a>' for h, t, c in items)
    return ('<a class="skip" href="#main">Skip to content</a>\n<header class="top"><div class="wide">'
            f'<a class="mark" href="index.html"><i></i>Shaw Labs</a><nav class="nav" aria-label="Site">{links}</nav></div></header>')

FOOT = ('<footer class="foot"><div class="wide"><span>Shaw Labs is the workshop of Suraj Shaw, London.</span>'
        '<nav aria-label="Elsewhere"><a href="https://www.shawsuraj.com" rel="me">shawsuraj.com</a><a href="https://github.com/shawsuraj" rel="me">GitHub</a>'
        '<a href="https://www.linkedin.com/in/shawsuraj/" rel="me">LinkedIn</a><a href="mailto:shaw@shawsuraj.com">Email</a></nav></div></footer>')

def head(meta, slug, full):
    url = HOST + ("/" if slug == "index" else "/" + slug)
    h = [f'<title>{meta["title"]}</title>', '<meta name="claude:viewport-fit-sides" content="cover">',
         f'<meta name="description" content="{meta["desc"]}">', FONTS, f'<link rel="icon" href="{ICON}">']
    if full:
        h += [f'<link rel="canonical" href="{url}">', f'<meta property="og:type" content="{"website" if slug=="index" else "article"}">',
              f'<meta property="og:title" content="{meta["title"]}">', f'<meta property="og:description" content="{meta["desc"]}">',
              f'<meta property="og:url" content="{url}">', f'<meta property="og:image" content="{HOST}/assets/og.jpg">',
              '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
              '<meta name="twitter:card" content="summary_large_image">', '<meta name="twitter:site" content="@shawsurajss">',
              '<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">',
              '<meta name="theme-color" content="#101114" media="(prefers-color-scheme: dark)">']
    h.append(f"<style>{CSS}</style>")
    return "\n".join(h)

def page(slug, full):
    first, body = open(os.path.join(SRC, "pages", slug + ".html")).read().split("\n", 1)
    meta = json.loads(first)
    has_explorer = "{{EXPLORER}}" in body
    body = body.replace("{{EXPLORER}}", EXPLORER_HTML).replace("{{CHART}}", CHART).replace("{{SHELF}}", shelf_html())
    content = f'{nav(meta["nav"])}\n<main id="main">\n{body}\n</main>\n{FOOT}'
    if has_explorer:
        content += f"\n<script>{EXPLORER_JS}</script>"
    if "data-wcm" in body:
        content += f"\n<script>{BENCH_JS}</script>"
    if full:
        content = re.sub(r'href="index\.html(#[^"]*)?"', lambda m: f'href="/{m.group(1) or ""}"', content)
        content = re.sub(r'href="(world-chaos-map|building-in-public)\.html(#[^"]*)?"', lambda m: f'href="/{m.group(1)}{m.group(2) or ""}"', content)
        return (f'<!doctype html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n'
                f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head(meta, slug, True)}\n</head>\n'
                f'<body>\n{content}\n</body>\n</html>\n')
    if slug == "index":
        return head(meta, slug, False) + "\n" + content
    return (f'<!doctype html>\n<html lang="en-GB"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head(meta, slug, False)}</head><body>\n{content}\n</body></html>\n')

for target, full in (("dist", True), ("preview", False)):
    out = os.path.join(ROOT, target)
    os.makedirs(out, exist_ok=True)
    for slug in PAGES:
        open(os.path.join(out, slug + ".html"), "w").write(page(slug, full))
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(out, "assets"), dirs_exist_ok=True)
    if full:
        for f in ("vercel.json", "robots.txt", "sitemap.xml"):
            shutil.copy(os.path.join(ROOT, f), out)
print("built")
