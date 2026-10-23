"""Builds shawlabs.dev into dist/ (Vercel) and preview/ (Claude preview).
Each page in src/pages starts with one line of JSON metadata."""
import json, os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
CSS = open(os.path.join(SRC, "styles.css")).read()
HOST = "https://www.shawlabs.dev"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800'
         '&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=JetBrains+Mono:wght@400;500&display=swap">')
ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%23142047'/%3E"
        "%3Cpath d='M26 14h12M28 14v14L17 48a4 4 0 0 0 3.5 6h23A4 4 0 0 0 47 48L36 28V14' fill='none' stroke='%23f3f4ef' stroke-width='4' stroke-linejoin='round'/%3E"
        "%3Ccircle cx='32' cy='44' r='4' fill='%23d0473a'/%3E%3C/svg%3E")
FLASK = ('<svg class="flask" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M9 3h6M10 3v6L4.5 18.5A1.7 1.7 0 0 0 6 21h12a1.7 1.7 0 0 0 1.5-2.5L14 9V3"/><path d="M7.5 15h9"/></svg>')
PAGES = [("index", "Lab"), ("world-chaos-map", "SL-03 World Chaos Map")]

def nav(current):
    links = [('index.html', 'Lab', current == 'index'), ('index.html#experiments', 'Experiments', False),
             ('world-chaos-map.html', 'Case study', current == 'world-chaos-map'), ('index.html#notes', 'Notes', False)]
    items = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if cur else ""}>{t}</a>' for h, t, cur in links)
    items += '<a href="https://www.shawsuraj.com" rel="me">shawsuraj.com</a>'
    return ('<a class="skip" href="#main">Skip to content</a>\n<header class="top"><div class="wrap">'
            f'<a class="mark" href="index.html">{FLASK}Shaw Labs</a><nav class="nav" aria-label="Site">{items}</nav></div></header>')

FOOT = '''<footer class="foot"><div class="wrap page">
<div class="row"><h2>Shaw Labs.</h2>
<nav aria-label="Elsewhere"><a href="https://www.shawsuraj.com" rel="me">shawsuraj.com</a><a href="https://github.com/shawsuraj" rel="me">GitHub</a><a href="https://www.linkedin.com/in/shawsuraj/" rel="me">LinkedIn</a><a href="mailto:shaw@shawsuraj.com">shaw@shawsuraj.com</a></nav></div>
<small>The lab of Suraj Shaw, London. Built by hand, no trackers.</small>
</div></footer>'''

def head(meta, slug, full):
    url = HOST + ("/" if slug == "index" else "/" + slug)
    h = [f'<title>{meta["title"]}</title>', '<meta name="claude:viewport-fit-sides" content="cover">',
         f'<meta name="description" content="{meta["desc"]}">', FONTS, f'<link rel="icon" href="{ICON}">']
    if full:
        h += [f'<link rel="canonical" href="{url}">', '<meta property="og:type" content="website">',
              f'<meta property="og:title" content="{meta["title"]}">', f'<meta property="og:description" content="{meta["desc"]}">',
              f'<meta property="og:url" content="{url}">', f'<meta property="og:image" content="{HOST}/assets/og.jpg">',
              '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
              '<meta name="twitter:card" content="summary_large_image">', '<meta name="twitter:site" content="@shawsurajss">',
              '<meta name="theme-color" content="#f3f4ef" media="(prefers-color-scheme: light)">',
              '<meta name="theme-color" content="#0c1830" media="(prefers-color-scheme: dark)">']
    h.append(f"<style>{CSS}</style>")
    return "\n".join(h)

def page(slug, full):
    raw = open(os.path.join(SRC, "pages", slug + ".html")).read()
    first, body = raw.split("\n", 1)
    meta = json.loads(first)
    content = f'{nav(slug)}\n<main id="main">\n{body}\n</main>\n{FOOT}'
    if full:
        content = re.sub(r'href="index\.html(#[^"]*)?"', lambda m: f'href="/{m.group(1) or ""}"', content)
        content = re.sub(r'href="(world-chaos-map)\.html(#[^"]*)?"', lambda m: f'href="/{m.group(1)}{m.group(2) or ""}"', content)
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
    for slug, _ in PAGES:
        open(os.path.join(out, slug + ".html"), "w").write(page(slug, full))
    if os.path.isdir(os.path.join(ROOT, "assets")):
        shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(out, "assets"), dirs_exist_ok=True)
    if full:
        for f in ("vercel.json", "robots.txt", "sitemap.xml"):
            if os.path.exists(os.path.join(ROOT, f)):
                shutil.copy(os.path.join(ROOT, f), out)
print("built")
