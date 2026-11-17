#!/usr/bin/env python3
"""Builds lastround.shawlabs.dev into public/.

Plain static pages. No JavaScript, no third-party requests, fonts served from
this site (docs/website.md: a privacy page that tracks its readers undoes itself).
"""
import os, shutil, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "public")
HOST = "https://lastround.shawlabs.dev"
EMAIL = "lastround@shawlabs.dev"
UPDATED = "17 November 2026"

CSS = open(os.path.join(SRC, "site.css")).read()

NAV = [("/", "Home"), ("/privacy", "Privacy"), ("/help", "Help"), ("/support", "Support")]


def page(slug, title, desc, body, wide=False):
    path = "/" if slug == "index" else "/" + slug
    nav = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == path else ""}>{t}</a>' for h, t in NAV
    )
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{HOST}{path}">
<meta name="theme-color" content="#2A1A10">
<meta name="color-scheme" content="dark">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{HOST}{path}">
<meta property="og:type" content="website">
<meta property="og:image" content="{HOST}/og.png">
<link rel="icon" href="/app-icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/unbounded.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/instrument-sans.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style>
</head>
<body>
<div class="bokeh" aria-hidden="true"><i></i><i></i><i></i></div>
<header class="top">
  <a class="mark" href="/" aria-label="Last Round home"><img src="/launch-mark.svg" alt="" width="40" height="40"><span>last round</span></a>
  <nav aria-label="Main">{nav}</nav>
</header>
<main class="{'wide' if wide else 'col'}">
{body}
</main>
<footer class="foot">
  <p>18+ only. Last Round is not medical advice. If you are worried about your drinking, <a href="/help">help is here</a>.</p>
  <p class="links"><a href="/privacy">Privacy</a><a href="/alpha">Alpha terms</a><a href="/support">Support</a><a href="/help">Help</a><a href="https://www.shawlabs.dev">A Shaw Labs project</a></p>
</footer>
</body>
</html>
"""


INDEX = f"""
<section class="hero">
  <div class="hero-text">
    <p class="chip">In alpha · invite only · iPhone and Android</p>
    <h1>Good nights,<br>well kept.</h1>
    <p class="lede">A drink tracker for nights out. Log any drink in two taps, earn points for a good pace and for water, and wake up to a receipt and a map of where the night went.</p>
    <p class="sub">Your nights stay on your phone. No account, no ads, nothing sent to us.</p>
  </div>
  <img class="icon" src="/app-icon.svg" alt="The Last Round app icon: a pint glass on a wooden bar under warm amber light" width="260" height="260">
</section>

<section class="paper rules" aria-labelledby="rules">
  <p class="kicker">House rules</p>
  <h2 id="rules">Three, and they are short.</h2>
  <ol>
    <li><b>It stays on your phone.</b> No account, no ads, nothing sent to us. On iPhone the map comes from Apple Maps; that is the only thing that ever goes online.</li>
    <li><b>Water earns points.</b> Have a water between drinks and tap Water. It scores from ten minutes after your last drink.</li>
    <li><b>Two taps a drink.</b> Tap Drink, tap what you are having. Same again is one.</li>
  </ol>
</section>

<section class="split">
  <div>
    <h2>How the points work</h2>
    <ul class="plain">
      <li><b>A good pace scores.</b> Each drink earns points, and so does each water break in between.</li>
      <li><b>There are caps, by the hour, the night and the week.</b> Past one, points simply stop. You will never see a number, a bar or a countdown to a cap, because a visible ceiling becomes a target.</li>
      <li><b>You can set your own weekly limit.</b> It caps your points too, and it cannot be switched off on a whim mid-night.</li>
      <li><b>Alerts wait for a pause.</b> At most one an hour, each at most once a night. They read as care, never as a telling-off.</li>
      <li><b>The morning after, you get a receipt.</b> Where you went, how long you were out, your water breaks and your points.</li>
    </ul>
  </div>
  <figure class="receipt" aria-label="An example receipt">
    <p class="r-head">LAST ROUND</p>
    <p class="r-sub">Example receipt</p>
    <p class="r-sub">Printed for Alex</p>
    <p class="r-rule"></p>
    <p><span>Fri 14 Nov</span><span>The Crown</span></p>
    <p><span>Home by</span><span>23:30</span></p>
    <p><span>Out</span><span>3h 10m</span></p>
    <p><span>Water breaks</span><span>3</span></p>
    <p class="r-rule"></p>
    <p class="r-total"><span>Points</span><span>42</span></p>
    <p class="r-rule"></p>
    <p class="r-note">Kept the pace.</p>
    <p class="r-note">Thank you, come again.</p>
  </figure>
</section>

<section class="inalpha" aria-labelledby="inalpha">
  <p class="kicker">In the alpha</p>
  <h2 id="inalpha">What you get on night one.</h2>
  <div class="feats">
    <div class="feat feat-map">
      <img class="phone" src="/screen-map.webp" alt="The Map tab in Last Round: an amber glow over Covent Garden, amber badges for the bars you have been to, and wood badges for bars nearby" width="560" height="1131" loading="lazy">
      <div>
      <h3>A map of your nights</h3>
      <p>Every bar you have had a night in, with how many nights. A soft amber glow spreads over the streets you go out in. Tap a bar for its receipts, or Drink here to start. iPhone first; Android gets a list of your places.</p>
      </div>
    </div>
    <div class="feat"><h3>Pick the bar</h3><p>Start a night and the bars near you are already there, with the ones you have been to before at the top. Or just type the name.</p></div>
    <div class="feat"><h3>A calendar, not a streak</h3><p>Your weeks, months and year at a glance, shaded amber by the night, with a teal dot for water. No streak to keep alive.</p></div>
    <div class="feat"><h3>The receipt</h3><p>The morning after, a printed receipt with your name on it: where you went, how long you were out, water breaks and points.</p></div>
    <div class="feat"><h3>Share a night</h3><p>Turn a night into a picture for your story. Place, time out, water breaks. Never how many drinks.</p></div>
    <div class="feat"><h3>Care, not nagging</h3><p>A reminder of the plan you set and a water nudge, both off until you turn them on. Links to real help are always one tap away.</p></div>
  </div>
</section>

<section class="paper bench" aria-labelledby="bench">
  <p class="kicker">On the bench</p>
  <h2 id="bench">Being built for the first invites.</h2>
  <ul>
    <li><b>The night moves with you.</b> Tap Moved bar and the night becomes a route: every bar, in order, on the receipt and the map.</li>
    <li><b>Passport stamps.</b> A stamp for each new bar, city and country, and a globe that fills in amber where you have had a night out.</li>
    <li><b>Coasters.</b> A coaster for every bar you visit, its design drawn from the bar's name, so no two are the same.</li>
    <li><b>Behind the bar.</b> A short card on what is in your drink and where it comes from, written by someone who poured them for years.</li>
    <li><b>The morning outlook.</b> One honest line on the receipt, like "A slow start likely. Water and breakfast first."</li>
    <li><b>Never open the app.</b> Same again and water from the Lock Screen, a Live Activity with the bar and time out, and Siri: "add a Guinness".</li>
  </ul>
  <p class="small">Some of these may land a build or two into the alpha. Testers get every build as it ships.</p>
</section>

<section class="split asks">
  <div>
    <h2>What testers help answer</h2>
    <ul class="plain">
      <li><b>Do the caps feel fair?</b> Or do they get in the way of a good night?</li>
      <li><b>Do points get people drinking water?</b> The whole idea rests on this one.</li>
      <li><b>Do the alerts feel like care?</b> Or like being told off?</li>
      <li><b>Is the receipt worth opening the morning after?</b></li>
    </ul>
  </div>
  <div class="note-card">
    <p>No analytics, so nothing is learned behind your back. Two short forms, after week one and week four, and a group chat for bugs. That is how the app gets better.</p>
  </div>
</section>

<section class="paper never" aria-labelledby="never">
  <h2 id="never">What it will never do</h2>
  <ul>
    <li>Rank, reward or show off how much anyone drinks.</li>
    <li>Show a countdown, bar or ring towards a cap.</li>
    <li>Send your nights anywhere, or write them to Apple Health or Health Connect.</li>
    <li>Put you on a map for anyone else. No friends on the map, no live location.</li>
    <li>Track you. No analytics, no ads, no account.</li>
  </ul>
</section>

<section class="status">
  <h2>Where it is</h2>
  <div class="steps">
    <div class="now"><p class="kicker">Now</p><h3>Alpha</h3><p>About fifteen friends, invited a few at a time, for four weeks of real nights out. iPhone through TestFlight, Android through Play testing, both from the same build.</p></div>
    <div><p class="kicker">Next</p><h3>Beta</h3><p>A wider test. Water breaks checked by your phone's camera, on the phone itself, with the clip deleted straight after. A bar passport, and a year of nights wrapped up to share.</p></div>
  </div>
  <p class="ask">Want in on the beta? Email <a href="mailto:{EMAIL}?subject=Last%20Round%20beta">{EMAIL}</a>. You must be 18 or over.</p>
</section>

<section class="maker">
  <p>Made by <a href="https://www.shawsuraj.com">Suraj Shaw</a> at <a href="https://www.shawlabs.dev">Shaw Labs</a>, after five years behind London bars.</p>
</section>
"""

PRIVACY = f"""
<article class="doc">
<p class="kicker">Last updated {UPDATED}</p>
<h1>Privacy</h1>
<p class="lede">Everything you log in Last Round stays on your phone. Nothing is sent to us. This page says exactly what is kept, where, and the one thing that talks to Apple Maps on iPhone.</p>

<h2>Who we are</h2>
<p>Last Round is made by Shaw Labs, run by Suraj Shaw in London. For any privacy question, email <a href="mailto:{EMAIL}?subject=Last%20Round%20privacy">{EMAIL}</a>.</p>

<h2>What the app keeps, only on your phone</h2>
<ul>
  <li>Each drink and water break, with its time.</li>
  <li>The place you type for a night or, on iPhone, the bar you pick from the suggestions, with where that bar is (its map point and Apple Maps' id for it). And your plan, such as the time you mean to be home.</li>
  <li>Your name, if you set one. It is printed on your receipts and never on a picture you share.</li>
  <li>Your weekly limit, which alerts you have seen, and how long you keep your nights.</li>
  <li>For your age, a yes and when you tapped it. Never your date of birth.</li>
</ul>

<h2>What we never collect</h2>
<p>No account, no analytics, no ads and no tracking. No contacts and no health data. Nothing is sent to a server of ours, because there is none. Where you are is never stored. On Android the app has no internet or location permission.</p>

<h2>Bar suggestions and the map (iPhone only)</h2>
<p>On iPhone you can turn on <i>Suggest bars near me</i> in You, or by answering yes the first time you open the Map tab. It is off until you do. When it is on and you start a night or open the Map tab, the app asks iPhone for your location once and uses Apple Maps to list bars near you. If you search, what you type goes to Apple Maps too, and tapping one of Apple's bar labels or <i>Search this area</i> asks Apple about that place or that part of the map.</p>
<p>Apple handles that request under Apple's own privacy policy. It does not come to us, and your location is never saved: only the bar you pick, and where that bar is, is kept with that night on your phone. Delete everything removes it, and the setting goes back to off. Android does not have this feature and asks for no location.</p>
<p>How far each suggested bar is shows on screen only and is never saved. The map on iPhone (the Map tab, and the map from the Start sheet) is drawn by Apple Maps, so the area you are looking at is sent to Apple to draw it, even with suggestions off. With suggestions on, opening the map reads your location once and marks where you were. The map never follows you, and the mark goes when you leave the map. Your map is drawn from the bars you picked, kept on your phone.</p>

<h2>Backups</h2>
<p>On iPhone, the app's data is kept out of iCloud and Finder backups. On Android, app backup is turned off. So your nights are not copied to any cloud.</p>

<h2>How long nights are kept</h2>
<p>Whole nights older than the period you pick are deleted on the phone. You can choose 30 days, 3 months, 6 months or 12 months. It is 12 months unless you change it. Your most recent night stays until a newer one, or until you delete everything.</p>

<h2>Your controls</h2>
<ul>
  <li><b>Delete everything</b> wipes the phone's copy at once. One thing stays for up to a day: a weekly limit you set yourself. That is on purpose, so deleting cannot be used to get around a limit you chose.</li>
  <li><b>Export my nights</b> makes a JSON file, your name included, that you save wherever you choose. That copy is then yours to keep or delete.</li>
</ul>

<h2>Notifications</h2>
<p>The plan reminder and the water nudge are both off until you turn them on. They are set on your phone, not sent from a server, and never name a drink.</p>

<h2>Sharing a night</h2>
<p>Share your night makes a picture on your phone, only when you tap it, and hands it to your phone's share sheet. Where it goes after that is up to you. It never shows your name, your points or a limit.</p>

<h2>Links out</h2>
<p>The Drinkaware, NHS, Drinkline and Samaritans links in the app open in your browser or phone app. Last Round sends nothing with them. Those services have their own privacy policies.</p>

<h2>Age</h2>
<p>Last Round is for adults aged 18 and over. It is not for children.</p>

<h2>Our legal basis</h2>
<p>Because nothing you log ever reaches us, we do not collect or process it, and we are not a controller of the data kept on your phone. If you email us, we use your email address and message only to reply, on the basis of our legitimate interest in answering you, and we delete them when the conversation is over.</p>

<h2>This website</h2>
<p>This site sets no cookies and runs no analytics or third-party scripts. Its fonts are served from this site. Our host, Vercel, keeps standard server logs, such as IP addresses, for a short time to run and secure the site.</p>

<h2>Changes</h2>
<p>If this policy changes, the date at the top changes with it, and testers hear about it in the alpha group before the build that needs it.</p>
</article>
"""

ALPHA = f"""
<article class="doc">
<p class="kicker">Last updated {UPDATED}</p>
<h1>Alpha terms</h1>
<p class="lede">Thank you for testing Last Round. By installing the alpha, you agree to the following.</p>
<ul>
  <li><b>You are 18 or over.</b> Last Round tracks drinking and is for adults only.</li>
  <li><b>This is a test build.</b> It may have bugs, and it may lose your data. Do not rely on it for anything that matters.</li>
  <li><b>Drink responsibly.</b> Points are a game, not a goal. Never drink more to score, and never drive after drinking.</li>
  <li><b>No guarantees.</b> The alpha is given as it is, and it is not medical advice. If you are worried about your drinking, see <a href="/help">Help</a>.</li>
  <li><b>Your data stays yours.</b> Everything stays on your phone, as the <a href="/privacy">privacy policy</a> sets out.</li>
  <li><b>You can stop at any time.</b> Use Delete everything, then remove the app.</li>
</ul>
<h2>Reporting a bug</h2>
<p>Send a screenshot and what you tapped in the alpha WhatsApp group, or email <a href="mailto:{EMAIL}?subject=Last%20Round%20bug">{EMAIL}</a>. Every bug becomes a test before it is fixed.</p>
</article>
"""

SUPPORT = f"""
<article class="doc">
<h1>Support</h1>
<p class="lede">Something not working, or a question about the app? Email <a href="mailto:{EMAIL}?subject=Last%20Round%20support">{EMAIL}</a>. A person reads every message.</p>
<h2>Reporting a bug</h2>
<p>A screenshot plus what you tapped is perfect. Alpha testers can also post it in the alpha WhatsApp group.</p>
<h2>Your data</h2>
<p>We cannot see or recover your nights, because they never leave your phone. To remove everything, open You in the app and tap Delete everything. See the <a href="/privacy">privacy policy</a>.</p>
<h2>Help with drinking</h2>
<p>For advice or someone to talk to, see <a href="/help">Help and advice</a>.</p>
<h2>Credits</h2>
<p>Unbounded, Instrument Sans, IBM Plex Mono and DM Sans are used under the SIL Open Font License 1.1. The licences ship with the app and are on this site: <a href="/fonts/OFL-Unbounded.txt">Unbounded</a>, <a href="/fonts/OFL-InstrumentSans.txt">Instrument Sans</a>, <a href="/fonts/OFL-IBMPlexMono.txt">IBM Plex Mono</a>.</p>
</article>
"""

HELP = """
<article class="doc">
<h1>Help and advice</h1>
<p class="lede">Free and confidential. You do not need to use Last Round for any of these.</p>
<ul class="help">
  <li class="urgent"><a href="tel:999"><b>Call 999</b></a><span>If someone cannot be woken, or is breathing slowly or oddly. Stay with them.</span></li>
  <li><a href="https://www.nhs.uk/conditions/alcohol-poisoning/"><b>Signs of alcohol poisoning</b></a><span>NHS: what to look for and what to do.</span></li>
  <li><a href="tel:03001231110"><b>Drinkline 0300 123 1110</b></a><span>Free and confidential. Weekdays 9am to 8pm, weekends 11am to 4pm.</span></li>
  <li><a href="tel:116123"><b>Samaritans 116 123</b></a><span>Free, any time, day or night.</span></li>
  <li><a href="https://www.nhs.uk/live-well/alcohol-advice/"><b>NHS alcohol advice</b></a><span>The low-risk guideline and ways to cut down.</span></li>
  <li><a href="https://www.drinkaware.co.uk/"><b>Drinkaware</b></a><span>Independent advice on alcohol.</span></li>
  <li><a href="https://www.drinkaware.co.uk/facts/information-about-alcohol/alcoholic-drinks-and-units/what-is-an-alcohol-unit"><b>What a unit is</b></a><span>Drinkaware: the units in your drinks.</span></li>
  <li><a href="https://www.drinkaware.co.uk/advice-and-support/alcohol-support-services"><b>Support services</b></a><span>Drinkaware's list, for you or someone close.</span></li>
</ul>
<p class="note">These links leave this site. Last Round and this site send nothing with them.</p>
</article>
"""

PAGES = [
    ("index", "Last Round · Good nights, well kept", "A drink tracker for nights out. Two taps a drink, points for a good pace and for water, a receipt and a map of your nights, and everything kept on your phone. In alpha.", INDEX, True),
    ("privacy", "Privacy · Last Round", "What Last Round keeps, and where: everything stays on your phone and nothing is sent to us. On iPhone, bar suggestions and the map use Apple Maps.", PRIVACY, False),
    ("alpha", "Alpha terms · Last Round", "The terms for Last Round alpha testers: 18+, a test build, drink responsibly, no guarantees.", ALPHA, False),
    ("support", "Support · Last Round", "Get help with the Last Round app, report a bug, or ask about your data.", SUPPORT, False),
    ("help", "Help and advice · Last Round", "Free and confidential alcohol advice and support: 999, NHS, Drinkline, Samaritans and Drinkaware.", HELP, False),
]


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for name in ("screen-map.webp", "app-icon.svg", "launch-mark.svg", "og.png", "apple-touch-icon.png", "robots.txt"):
        p = os.path.join(SRC, name)
        if os.path.exists(p):
            shutil.copy(p, OUT)
    shutil.copytree(os.path.join(SRC, "fonts"), os.path.join(OUT, "fonts"))
    for slug, title, desc, body, wide in PAGES:
        with open(os.path.join(OUT, slug + ".html"), "w") as f:
            f.write(page(slug, title, desc, body, wide))
    urls = "".join(f"<url><loc>{HOST}{'/' if s == 'index' else '/' + s}</loc></url>" for s, *_ in PAGES)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    print("built", len(PAGES), "pages")


if __name__ == "__main__":
    main()
