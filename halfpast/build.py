#!/usr/bin/env python3
"""Builds halfpast.shawlabs.dev into public/.

Plain static pages. No JavaScript, no third-party requests, fonts served from
this site (docs/website.md: a privacy page that tracks its readers undoes itself).
"""
import os, shutil, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "public")
HOST = "https://halfpast.shawlabs.dev"
EMAIL = "halfpast@shawlabs.dev"
UPDATED = "24 November 2026"

# Sign-ups are open: /join shows the form. Set False to show the email route.
# The form posts to our own /api/join (api/join.js), which passes it on to the
# Apps Script web app (signups/SETUP.md) and sends the person to /thanks.
# Nobody sees a Google page, so it works in Instagram's in-app browser.
SIGNUP_OPEN = True
SIGNUP_ACTION = "/api/join"

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
<meta property="og:image" content="{HOST}/og-halfpast.png">
<link rel="icon" href="/app-icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/unbounded.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/instrument-sans.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style>
</head>
<body>
<div class="bokeh" aria-hidden="true"><i></i><i></i><i></i></div>
<header class="top">
  <a class="mark" href="/" aria-label="Half Past home"><img src="/launch-mark.svg" alt="" width="40" height="40"><span>half past</span></a>
  <nav aria-label="Main">{nav}<a class="pill" href="/join">Join the alpha</a></nav>
</header>
<main class="{'story' if slug == 'index' else ('wide' if wide else 'col')}">
{body}
</main>
<footer class="foot">
  <p>18+ only. Half Past is not medical advice. If you are worried about your drinking, <a href="/help">help is here</a>.</p>
  <p class="links"><a href="/privacy">Privacy</a><a href="/alpha">Alpha terms</a><a href="/support">Support</a><a href="/help">Help</a><a href="https://www.shawlabs.dev">A Shaw Labs project</a></p>
</footer>
</body>
</html>
"""


def clock(hhmm):
    """A small bar clock showing the time of each beat of the night."""
    h, m = (int(x) for x in hhmm.split(":"))
    ha, ma = (h % 12 + m / 60) * 30, m * 6
    return (f'<svg class="clock" viewBox="0 0 40 40" width="40" height="40" aria-hidden="true">'
            f'<circle cx="20" cy="20" r="17"/>'
            f'<line x1="20" y1="20" x2="20" y2="10" transform="rotate({ha:.1f} 20 20)"/>'
            f'<line class="min" x1="20" y1="20" x2="20" y2="6" transform="rotate({ma:.1f} 20 20)"/>'
            f'<circle class="pin" cx="20" cy="20" r="2"/></svg>')


def when(hhmm, label):
    return f'<p class="when">{clock(hhmm)}<span>{label}</span></p>'


def shot(name, alt, cls="", eager=False):
    """A real screenshot from the app, in a phone."""
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="phone {cls}" src="/shots/{name}-480.webp" '
            f'srcset="/shots/{name}-480.webp 480w, /shots/{name}-860.webp 860w" '
            f'sizes="(min-width: 900px) 320px, 62vw" width="1320" height="2868" alt="{html.escape(alt)}" {load}>')


INDEX = f"""
<section class="hero">
  <div class="wrap hero-in">
    <div class="hero-text">
      {when("19:30", "Friday. Getting ready.")}
      <h1>Good nights,<br><span>well kept.</span></h1>
      <p class="lede">A drinks tracker for nights out. Two taps a drink, points for a good pace, a receipt in the morning.</p>
      <p class="actions"><a class="cta" href="/join">Join the alpha</a><span class="fine">Free · iPhone and Android · 18+</span></p>
    </div>
    <div class="fan" aria-label="Three screens from the app">
      {shot("receipt", "The morning-after receipt for a night at Panda and Sons: 79 points", "f1", True)}
      {shot("welcome", "The Half Past welcome screen: three glasses on a wooden shelf and the words Good nights, well kept", "f2", True)}
      {shot("live", "A night in progress: 41 points, an Edinburgh Gin just logged, Drink and Water buttons", "f3", True)}
    </div>
  </div>
  <div class="ledge" aria-hidden="true"></div>
</section>

<section class="beat">
  <div class="wrap beat-in">
    <div class="copy rise">
      {when("19:45", "Out the door")}
      <h2>Out tonight?</h2>
      <p>One tap starts the night. Your last night out is right there to beat.</p>
    </div>
    <div class="phones">{shot("home", "The Tonight tab: Out tonight? with last night's 79 points and a Start the night button", "rise")}</div>
  </div>
</section>

<section class="beat flip">
  <div class="wrap beat-in">
    <div class="copy rise">
      {when("20:16", "First round")}
      <h2>Two taps<br>a drink.</h2>
      <p>The whole menu, from a pint to a Passion fruit martini. Same again is one tap.</p>
    </div>
    <div class="phones pair">
      {shot("live", "Points tonight: 41, with the Edinburgh Gin just logged", "rise back")}
      {shot("menu", "The drink menu: cocktails with their strength and units, Same again at the top", "rise front")}
    </div>
  </div>
</section>

<section class="beat water">
  <div class="wrap beat-in">
    <div class="copy rise">
      {when("20:41", "Between rounds")}
      <h2>Water scores too.</h2>
      <p>A glass between rounds earns points. Pace is the game, and the best nights win it.</p>
    </div>
    <div class="phones pair">
      {shot("water", "The water break screen: a teal ring and Tap to log it", "rise back")}
      {shot("water-logged", "Water logged, plus 7 points, 48 points tonight", "rise front")}
    </div>
  </div>
</section>

<section class="interval">
  <div class="wrap">
    {when("23:25", "Last orders")}
    <p class="big rise">Tap End night.<br><span>Go home.</span></p>
  </div>
</section>

<section class="beat morning">
  <div class="wrap beat-in">
    <div class="copy rise">
      {when("09:10", "The morning after")}
      <h2>Here is<br>your night.</h2>
      <p>A printed receipt: where you went, how long you were out, how you paced it. Share it to your story, with the drinks hidden if you like.</p>
    </div>
    <div class="phones pair">
      {shot("receipt", "The receipt: Panda and Sons, 19:45 to 23:25, 79 points, Thanks for keeping it good", "rise back")}
      {shot("share", "Share your night, with switches to show the drinks and the place", "rise front")}
    </div>
  </div>
</section>

<section class="beat flip">
  <div class="wrap beat-in">
    <div class="copy rise">
      {when("12:00", "Sunday")}
      <h2>Every night,<br>kept.</h2>
      <p>Your nights in one list, and a calendar shaded by the night. No streaks to keep alive.</p>
    </div>
    <div class="phones pair">
      {shot("nights", "Your nights: 936 points, 14 nights, 31 water breaks, with a list of nights out", "rise back")}
      {shot("calendar", "The calendar for November, each night shaded by units", "rise front")}
    </div>
  </div>
</section>

<section class="atlas">
  <div class="wrap">
    <div class="copy rise">
      {when("00:00", "Every night so far")}
      <h2>Everywhere you<br>have had a round.</h2>
      <p>A map of your bars and a passport of the countries you have had a night out in. It is yours alone. Nobody else is on it, and nobody sees it.</p>
    </div>
    <div class="phones trio">
      {shot("map", "The map: amber pins for bars in India", "rise back")}
      {shot("passport", "Your passport: India, Japan, the United Kingdom, Germany and Portugal, with the bar and date of each first night", "rise front")}
    </div>
    <p class="fine center">Map and passport arrive on iPhone first. Android follows.</p>
  </div>
</section>

<section class="promise">
  <div class="wrap">
    <p class="kicker">House rules</p>
    <h2 class="rise">Yours, not ours.</h2>
    <ol class="vows">
      <li class="rise"><b>It stays on your phone.</b> Your nights never leave it.</li>
      <li class="rise"><b>No account.</b> No sign-in, no email, no password.</li>
      <li class="rise"><b>No ads. No tracking.</b> Nothing is sent to us. <a href="/privacy">The full privacy policy</a>.</li>
    </ol>
  </div>
</section>

<section class="board" aria-labelledby="road">
  <div class="wrap">
    <div class="chalk rise">
      <h2 id="road">Coming up</h2>
      <ol class="road">
        <li class="on"><span class="tag">Now</span><b>Alpha</b><span>Invite only. Friends first, a few at a time, for four weeks of real nights out. iPhone and Android.</span></li>
        <li><span class="tag">Next</span><b>Beta</b><span>Details soon.</span></li>
        <li><span class="tag">Then</span><b>App Store and Google Play</b><span>For everyone over 18.</span></li>
      </ol>
    </div>
  </div>
</section>

<section class="last" id="join">
  <div class="wrap">
    <h2 class="rise">Pull up a stool.</h2>
    <p>Test the alpha. Sign-up takes a minute.</p>
    <p><a class="cta big" href="/join">Join the alpha</a></p>
    <p class="maker">Made by <a href="https://www.shawsuraj.com">Suraj Shaw</a> at <a href="https://www.shawlabs.dev">Shaw Labs</a>, after five years behind London bars.</p>
  </div>
</section>
"""


PRIVACY = f"""
<article class="doc">
<p class="kicker">Last updated {UPDATED}</p>
<h1>Privacy</h1>
<p class="lede">Everything you log in Half Past stays on your phone. Nothing is sent to us. This page says exactly what is kept, where, and what the map and bar search send to Apple or Google.</p>

<h2>Who we are</h2>
<p>Half Past is made by Shaw Labs, run by Suraj Shaw in London. For any privacy question, email <a href="mailto:{EMAIL}?subject=Half%20Past%20privacy">{EMAIL}</a>.</p>

<h2>What the app keeps, only on your phone</h2>
<ul>
  <li>Each drink and water break, with its time.</li>
  <li>The place you type for a night, or the bar you pick from the suggestions, with where that bar is: its map point and the map service's id for it (Apple Maps' on iPhone, Google's on Android). And your plan, such as the time you mean to be home.</li>
  <li>Your name, if you set one. It is printed on your receipts and never on a picture you share.</li>
  <li>Your weekly limit, which alerts you have seen, and how long you keep your nights.</li>
  <li>For your age, a yes and when you tapped it. Never your date of birth.</li>
</ul>

<h2>What we never collect</h2>
<p>No account, no analytics, no ads and no tracking. No contacts and no health data. Nothing is sent to a server of ours, because there is none. Where you are is never stored.</p>

<h2>Bar suggestions and the map on iPhone</h2>
<p>You can turn on <i>Suggest bars near me</i> in You, or by answering yes the first time you open the Map tab. It is off until you do. When it is on and you start a night or open the Map tab, the app asks iPhone for your location once and uses Apple Maps to list bars near you. During a night, coming back to the app checks your location once more to ask if you have moved on to a new bar. That check stays on your phone and is sent to no one.</p>
<p>If you search, what you type goes to Apple Maps too, and <i>Search this area</i> asks Apple about that part of the map. Apple handles those requests under Apple's own privacy policy. They do not come to us, and your location is never saved: only the bar you pick, and where that bar is, is kept with that night on your phone. Delete everything removes it, and the setting goes back to off.</p>
<p>How far each suggested bar is shows on screen only and is never saved. The map (the Map tab, and the map from the Start sheet) is drawn by Apple Maps, so the area you are looking at is sent to Apple to draw it, even with suggestions off. With suggestions on, opening the map reads your location once and marks where you were. The map never follows you, and the mark goes when you leave the map. Your map is drawn from the bars you picked, kept on your phone.</p>

<h2>Bar suggestions and the map on Android</h2>
<p>It works the same way, with Google in Apple's place. The first time a search needs your location, Android asks whether Half Past may use it while the app is open, and you can choose approximate. Your location and anything you type to search go to Google's Places API to find bars. The map is drawn by Google Maps through Google Play services, so the area you are looking at is sent to Google, even with suggestions off. Google handles those requests under Google's own privacy policy, and Google Play services works under Google's own terms. None of it comes to us.</p>

<h2>Notice when I leave a bar</h2>
<p>This is off until you turn it on, and it needs notifications and location set to Always. While a night is open, your phone keeps one circle round tonight's bar and wakes Half Past only when you walk out of it, to send one notification that names no place, drink or number. On iPhone the circle is kept by iOS. On Android it is kept by Google Play services, under a plain name with no time or place in it. The circle is removed when the night ends. A night that closes itself while the app is away sends nothing, and its circle goes the next time you open the app or walk out. Where you go is never kept.</p>

<h2>Siri and Shortcuts</h2>
<p>If you use Siri, what you say is handled by Apple under Apple's own privacy policy, and Apple keeps its own history of it. Half Past cannot reach that history. The app keeps no record of a drink you named to Siri beyond the drink itself in your night.</p>

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
<p>The Drinkaware, NHS, Drinkline and Samaritans links in the app open in your browser or phone app. Half Past sends nothing with them. Those services have their own privacy policies.</p>

<h2>Age</h2>
<p>Half Past is for adults aged 18 and over. It is not for children.</p>

<h2>If you sign up for the alpha</h2>
<p>This is the one place we hold anything about you. The <a href="/join">sign-up form</a> asks for:</p>
<ul>
  <li>Your name and email address. Use the email on your Apple ID or Google account, because that is where the test invite goes.</li>
  <li>Whether you are on iPhone or Android.</li>
  <li>Your Instagram name, only if you choose to give it. It helps us tell who you are if we do not know your email.</li>
  <li>A yes that you are 18 or over, and a yes that you are happy to get emails about the alpha.</li>
</ul>
<p>We use it only to run the alpha: to send your invite through Apple's TestFlight or Google Play, to tell you about new builds and changes to these terms, and to send two short feedback forms, one after your first week and one at the end. We do not send marketing, and we never share or sell your details.</p>
<p>When you press Sign up, your answers pass through this site's host, Vercel, to a private Google Sheet kept by Suraj Shaw, through Google Apps Script. A short note about the sign-up is emailed to {EMAIL}. To send your invite, your email also goes to Apple or Google, whichever your phone uses. Vercel, Google and Apple act for us here under their own terms, and some of their servers are outside the UK, protected by the safeguards those terms set out. Only Suraj Shaw can see the sheet. Nothing you log in the app is ever added to it.</p>
<p>The alpha WhatsApp group is optional. If you join, everyone in the group can see your phone number and what you post, and WhatsApp handles it under its own privacy policy. We do not copy your number anywhere else. The two feedback forms are optional too, and each says what it asks before you start.</p>
<p>We delete your details, and the email notes about them, when the alpha ends, unless you ask to join the beta. If you leave early, tell us and we delete them then. You can see what we hold, correct it, or have it deleted at any time: email <a href="mailto:{EMAIL}?subject=Half%20Past%20sign-up">{EMAIL}</a>. Leaving the alpha does not affect anything on your phone.</p>
<p>If you are unhappy with how we handle your details, please tell us first. You also have the right to complain to the Information Commissioner's Office at <a href="https://ico.org.uk/make-a-complaint/">ico.org.uk</a>.</p>

<h2>Our legal basis</h2>
<p>Because nothing you log ever reaches us, we do not collect or process it, and we are not a controller of the data kept on your phone. For the alpha sign-up, we are the controller, and we rely on your consent, which you give with the two ticks on the form. You can withdraw it at any time by emailing us. If you email us, we use your email address and message only to reply, on the basis of our legitimate interest in answering you, and we delete them when the conversation is over.</p>

<h2>This website</h2>
<p>This site sets no cookies and runs no analytics or third-party scripts. Its fonts are served from this site. The sign-up form sends nothing until you press Sign up, and then only what you typed, through our host to Google as set out above. Our host, Vercel, keeps standard server logs, such as IP addresses, for a short time to run and secure the site.</p>

<h2>Changes</h2>
<p>If this policy changes, the date at the top changes with it, and testers hear about it in the alpha group before the build that needs it.</p>
</article>
"""

ALPHA = f"""
<article class="doc">
<p class="kicker">Last updated {UPDATED}</p>
<h1>Alpha terms</h1>
<p class="lede">Thank you for testing Half Past. By installing the alpha, you agree to the following.</p>
<p>Not in yet? <a href="/join">Sign up for the alpha</a>.</p>
<ul>
  <li><b>You are 18 or over.</b> Half Past tracks drinking and is for adults only.</li>
  <li><b>This is a test build.</b> It may have bugs, and it may lose your data. Do not rely on it for anything that matters.</li>
  <li><b>Drink responsibly.</b> Points are a game, not a goal. Never drink more to score, and never drive after drinking.</li>
  <li><b>No guarantees.</b> The alpha is given as it is, and it is not medical advice. If you are worried about your drinking, see <a href="/help">Help</a>.</li>
  <li><b>Your data stays yours.</b> Everything stays on your phone, as the <a href="/privacy">privacy policy</a> sets out.</li>
  <li><b>Signing up is not a place.</b> Invites go out in small groups, and not everyone who signs up gets one in this round.</li>
  <li><b>We may email you</b> about the alpha: your invite, news about new builds, changes to these terms, and two short feedback forms. Nothing else.</li>
  <li><b>Your sign-up details</b> (name, email, phone type and Instagram, if given) are used only to run the alpha and are deleted when it ends, as the <a href="/privacy">privacy policy</a> sets out.</li>
  <li><b>You can stop at any time.</b> Use Delete everything, then remove the app. Tell us if you want your sign-up details deleted too.</li>
</ul>
<h2>Reporting a bug</h2>
<p>Send a screenshot and what you tapped in the alpha WhatsApp group, or email <a href="mailto:{EMAIL}?subject=Half%20Past%20bug">{EMAIL}</a>. Every bug becomes a test before it is fixed.</p>
</article>
"""

SUPPORT = f"""
<article class="doc">
<h1>Support</h1>
<p class="lede">Something not working, or a question about the app? Email <a href="mailto:{EMAIL}?subject=Half%20Past%20support">{EMAIL}</a>. A person reads every message.</p>
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
<p class="lede">Free and confidential. You do not need to use Half Past for any of these.</p>
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
<p class="note">These links leave this site. Half Past and this site send nothing with them.</p>
</article>
"""

TESTING = f"""
<h2>How testing works</h2>
<ol class="howto">
  <li><b>You get an invite by email.</b> On iPhone it comes from Apple's TestFlight. On Android it is a Google Play testing link. Invites go out in small groups, so yours may take a little while.</li>
  <li><b>Use it on your nights out for about four weeks.</b> Log each drink, take water breaks, and open your receipt the morning after. Use it however feels natural. That is the test.</li>
  <li><b>Tell us what you think.</b> Your invite comes with a link to a small WhatsApp group for testers. Post anything there: what you like, what annoys you, what confuses you.</li>
  <li><b>Found a bug?</b> Send a screenshot and a line on what you tapped, in the group or to <a href="mailto:{EMAIL}?subject=Half%20Past%20bug">{EMAIL}</a>. That is all we need.</li>
  <li><b>Two short forms.</b> One after your first week and one at the end. A few minutes each, by email.</li>
  <li><b>The app tells us nothing on its own.</b> No analytics, no tracking. Your nights stay on your phone. We only learn what you choose to send.</li>
</ol>
<p>The full terms are on the <a href="/alpha">alpha page</a>. It is a test build, so things will break. Please drink responsibly.</p>
"""


def join_body(notice=""):
    """The sign-up page. A plain HTML form: no JavaScript, and nothing is sent
    anywhere until the person presses Sign up."""
    if notice:
        notice = f'<p class="notice" role="alert">{notice}</p>'
    if not SIGNUP_OPEN:
        form = f"""<p class="formcard">Sign-ups open here very soon. Until then, email <a href="mailto:{EMAIL}?subject=Half%20Past%20alpha">{EMAIL}</a> and say if you are on iPhone or Android.</p>"""
    else:
        form = f"""<form class="formcard" action="{SIGNUP_ACTION}" method="post" accept-charset="utf-8">
  <p class="field"><label for="name">Your name</label>
    <input id="name" name="name" type="text" autocomplete="name" maxlength="80" required></p>
  <p class="field"><label for="email">Email <span class="hint">Use the one on your Apple ID (iPhone) or Google account (Android). Your invite goes there.</span></label>
    <input id="email" name="email" type="email" autocomplete="email" inputmode="email" maxlength="120" required></p>
  <fieldset class="field"><legend>Which phone?</legend>
    <div class="choices">
      <label class="choice"><input type="radio" name="phone" value="iPhone" required><span>iPhone</span></label>
      <label class="choice"><input type="radio" name="phone" value="Android"><span>Android</span></label>
    </div>
  </fieldset>
  <p class="field"><label for="instagram">Instagram <span class="hint">Optional, so we know it is you.</span></label>
    <input id="instagram" name="instagram" type="text" autocomplete="off" autocapitalize="none" spellcheck="false" maxlength="40" placeholder="@yourname"></p>
  <label class="tick"><input type="checkbox" name="adult" value="yes" required><span>I am 18 or over.</span></label>
  <label class="tick"><input type="checkbox" name="emails" value="yes" required><span>I am happy to get emails about the alpha: my invite, news about new builds, and two short feedback forms.</span></label>
  <p class="trap" aria-hidden="true"><label for="website">Leave this empty</label><input id="website" name="website" type="text" tabindex="-1" autocomplete="off"></p>
  <p><button type="submit">Sign me up</button></p>
  <p class="small">We keep your details only to run the alpha, delete them when it ends, and never share them. Leave any time by emailing <a href="mailto:{EMAIL}?subject=Half%20Past%20sign-up">{EMAIL}</a>. See <a href="/privacy">privacy</a>.</p>
</form>"""
    return f"""
<article class="doc">
<p class="kicker">Alpha · 18+ only</p>
<h1>Join the alpha</h1>
<p class="lede">Half Past tracks your drinks and rewards a steady pace and water breaks. We are looking for 10 to 20 people to try it on real nights out, on iPhone or Android.</p>
{notice}
{form}
{TESTING}
</article>
"""


THANKS = f"""
<article class="doc">
<p class="kicker">Alpha</p>
<h1>You are on the list</h1>
<p class="lede">Thank you. We will email you when your invite is ready. Look out for an email from Apple (TestFlight) or Google Play.</p>
<p>Nothing after a while? Check your spam folder, or email <a href="mailto:{EMAIL}?subject=Half%20Past%20alpha">{EMAIL}</a>.</p>
{TESTING}
</article>
"""

PAGES = [
    ("index", "Half Past · Good nights, well kept", "A drink tracker for nights out. Two taps a drink, points for a good pace and for water, a receipt and a map of your nights, and everything kept on your phone. In alpha.", INDEX, True),
    ("privacy", "Privacy · Half Past", "What Half Past keeps, and where: everything stays on your phone and nothing is sent to us. Bar suggestions and the map use Apple Maps on iPhone and Google on Android.", PRIVACY, False),
    ("join", "Join the alpha · Half Past", "Sign up to test Half Past on your nights out, on iPhone or Android. 18+ only.", join_body(), False),
    ("alpha", "Alpha terms · Half Past", "The terms for Half Past alpha testers: 18+, a test build, drink responsibly, no guarantees.", ALPHA, False),
    ("support", "Support · Half Past", "Get help with the Half Past app, report a bug, or ask about your data.", SUPPORT, False),
    ("help", "Help and advice · Half Past", "Free and confidential alcohol advice and support: 999, NHS, Drinkline, Samaritans and Drinkaware.", HELP, False),
]


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for name in ("screen-map.webp", "app-icon.svg", "launch-mark.svg", "og-halfpast.png", "apple-touch-icon.png", "robots.txt"):
        p = os.path.join(SRC, name)
        if os.path.exists(p):
            shutil.copy(p, OUT)
    shutil.copytree(os.path.join(SRC, "fonts"), os.path.join(OUT, "fonts"))
    shutil.copytree(os.path.join(SRC, "shots"), os.path.join(OUT, "shots"))
    for slug, title, desc, body, wide in PAGES:
        with open(os.path.join(OUT, slug + ".html"), "w") as f:
            f.write(page(slug, title, desc, body, wide))
    # Pages the sign-up form returns to. Left out of the sitemap.
    extra = [
        ("thanks", "You are on the list · Half Past", "Thanks for signing up for the Half Past alpha.", THANKS, False),
        ("join-check", "Join the alpha · Half Past", "Sign up to test Half Past.",
         join_body("Something was missing or did not look right. Please check your answers and try again."), False),
        ("join-error", "Join the alpha · Half Past", "Sign up to test Half Past.",
         join_body(f'Something went wrong on our side, so your sign-up may not have saved. Please try again in a minute, or email <a href="mailto:{EMAIL}?subject=Half%20Past%20alpha">{EMAIL}</a>.'), False),
    ]
    for slug, title, desc, body, wide in extra:
        with open(os.path.join(OUT, slug + ".html"), "w") as f:
            f.write(page(slug, title, desc, body, wide))
    urls = "".join(f"<url><loc>{HOST}{'/' if s == 'index' else '/' + s}</loc></url>" for s, *_ in PAGES)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    print("built", len(PAGES), "pages")


if __name__ == "__main__":
    main()
