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
UPDATED = "22 November 2026"

# The Apps Script web app that receives the /join form (signups/SETUP.md).
# While it is empty, /join shows the email route instead of the form.
SIGNUP_URL = "https://script.google.com/macros/s/AKfycbzoxROz9ClZnRHltlf3ayOOsTMCDVWMfjTzgoLwqnZFXb9D_wGFoIjd-_Lda_Voi-6TZA/exec"
# vercel.json lets /join and /join-check post only to script.google.com and
# script.googleusercontent.com, where Apps Script redirects the post.

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
  <nav aria-label="Main">{nav}</nav>
</header>
<main class="{'wide' if wide else 'col'}">
{body}
</main>
<footer class="foot">
  <p>18+ only. Half Past is not medical advice. If you are worried about your drinking, <a href="/help">help is here</a>.</p>
  <p class="links"><a href="/privacy">Privacy</a><a href="/alpha">Alpha terms</a><a href="/support">Support</a><a href="/help">Help</a><a href="https://www.shawlabs.dev">A Shaw Labs project</a></p>
</footer>
</body>
</html>
"""


INDEX = f"""
<section class="hero">
  <div class="hero-text">
    <p class="chip">Alpha testers wanted · iPhone and Android</p>
    <h1>Good nights,<br>well kept.</h1>
    <p class="lede">A drink tracker for nights out. Log any drink in two taps, earn points for a good pace and for water, and wake up to a receipt and a map of where the night went.</p>
    <p class="sub">Your nights stay on your phone. No account, no ads, nothing sent to us.</p>
    <p><a class="cta" href="#join">Join the alpha</a></p>
  </div>
  <img class="icon" src="/app-icon.svg" alt="The Half Past app icon: a pint glass on a wooden bar under warm amber light" width="260" height="260">
</section>

<section class="paper rules" aria-labelledby="rules">
  <p class="kicker">House rules</p>
  <h2 id="rules">Three, and they are short.</h2>
  <ol>
    <li><b>It stays on your phone.</b> No account, no ads, nothing sent to us. The map and bar search come from Apple on iPhone and Google on Android. None of it comes to us.</li>
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
    <p class="r-head">HALF PAST</p>
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
  <h2 id="inalpha">What you get.</h2>
  <div class="feats">
    <div class="feat feat-map">
      <img class="phone" src="/screen-map.webp" alt="The Map tab in Half Past: an amber glow over Covent Garden, amber badges for the bars you have been to, and wood badges for bars nearby" width="560" height="1131" loading="lazy">
      <div>
      <h3>A map of your nights</h3>
      <p>Every bar you have had a night in, with how many nights. A soft amber glow spreads over the streets you go out in. Zoom out and a globe fills in amber where you have had a night out. Tap a bar for its receipts, or Drink here to start.</p>
      </div>
    </div>
    <div class="feat"><h3>Pick the bar</h3><p>Start a night and the bars near you are already there, with the ones you have been to before at the top. Or just type the name.</p></div>
    <div class="feat"><h3>The night moves with you</h3><p>Tap Moved bar and the night becomes a route: every bar, in order, on the receipt and the map.</p></div>
    <div class="feat"><h3>Stamps and coasters</h3><p>A stamp for each new bar, city and country. A coaster for every bar, its design drawn from the bar's name, so no two are the same.</p></div>
    <div class="feat"><h3>Behind the bar</h3><p>A short card on what is in your drink and where it comes from. Over seventy drinks so far.</p></div>
    <div class="feat"><h3>The receipt</h3><p>The morning after, a printed receipt with your name on it, and one honest line on how the morning might go, like "A slow start likely. Water and breakfast first."</p></div>
    <div class="feat"><h3>Never open the app</h3><p>Same again and water from a widget, the Lock Screen, a Live Activity or Quick Settings. Or ask Siri: "Add a drink in Half Past".</p></div>
    <div class="feat"><h3>A calendar, not a streak</h3><p>Your weeks, months and year at a glance, shaded amber by the night, with a teal dot for water. No streak to keep alive.</p></div>
    <div class="feat"><h3>Share a night</h3><p>Turn a night into a picture for your story. Place, time out, water breaks. Never how many drinks.</p></div>
    <div class="feat feat-wide"><h3>Care, not nagging</h3><p>A plan reminder, a water nudge, and, if you switch it on, a nudge when you leave a bar to log the next one or end the night. Links to real help are one tap away.</p></div>
  </div>
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
  <div class="steps three">
    <div class="now"><p class="kicker">Now</p><h3>Alpha</h3><p>Recruiting now. A small group of testers, let in a few at a time, for four weeks of real nights out. iPhone through TestFlight, Android through Play testing, both from the same build. Updates during the alpha bring your city and your year in places.</p></div>
    <div><p class="kicker">Next</p><h3>Beta</h3>
      <ul class="beta">
        <li><b>Water you can prove.</b> Your camera checks the water break, on the phone itself, and the clip is deleted straight after.</li>
        <li><b>Split the G.</b> Rate the pour, and see how close you get to the G. A bit of fun for Guinness drinkers.</li>
        <li><b>Wrapped.</b> Your year of nights out, the places and the water breaks, made to share.</li>
        <li><b>Little extras.</b> What the night cost, if you want to know, and badges for a good night: three water breaks, home by the plan, a new place.</li>
      </ul>
    </div>
    <div><p class="kicker">Later</p><h3>With friends</h3><p>Whose round it is, a water break for the whole table, and a "home safe" for the group. Each one waits for its own privacy review first, because it means a server, and today there is none.</p></div>
  </div>
  <p class="ask" id="join">Want to test the alpha? Sign-up takes a minute. You must be 18 or over.</p>
  <p><a class="cta" href="/join">Sign up for the alpha</a></p>
</section>

<section class="maker">
  <p>Made by <a href="https://www.shawsuraj.com">Suraj Shaw</a> at <a href="https://www.shawlabs.dev">Shaw Labs</a>, after five years behind London bars.</p>
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
  <li>Your Instagram name, only if you choose to give it.</li>
  <li>A yes that you are 18 or over, and a yes that you are happy to get emails about the alpha.</li>
</ul>
<p>We use it only to run the alpha: to send your invite through Apple's TestFlight or Google Play, to tell you about new builds and changes to these terms, and to send two short feedback forms, one after your first week and one at the end. We do not send marketing, and we never share or sell your details.</p>
<p>When you press Sign up, your answers go to a private Google Sheet kept by Suraj Shaw, through Google Apps Script, and a short note about the sign-up is emailed to {EMAIL}. Google handles that under Google's own terms. To send your invite, your email also goes to Apple or Google, whichever your phone uses. Nothing you log in the app is ever added to it.</p>
<p>We delete your details when the alpha ends, unless you ask to join the beta. You can see what we hold, correct it, or have it deleted at any time: email <a href="mailto:{EMAIL}?subject=Half%20Past%20sign-up">{EMAIL}</a>. Leaving the alpha does not affect anything on your phone.</p>

<h2>Our legal basis</h2>
<p>Because nothing you log ever reaches us, we do not collect or process it, and we are not a controller of the data kept on your phone. For the alpha sign-up, we are the controller, and we rely on your consent, which you give with the two ticks on the form. You can withdraw it at any time by emailing us. If you email us, we use your email address and message only to reply, on the basis of our legitimate interest in answering you, and we delete them when the conversation is over.</p>

<h2>This website</h2>
<p>This site sets no cookies and runs no analytics or third-party scripts. Its fonts are served from this site. The sign-up form sends nothing until you press Sign up, and then only what you typed, to Google as set out above. Our host, Vercel, keeps standard server logs, such as IP addresses, for a short time to run and secure the site.</p>

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
  <li><b>You can stop at any time.</b> Use Delete everything, then remove the app.</li>
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
    if not SIGNUP_URL:
        form = f"""<p class="formcard">Sign-ups open here very soon. Until then, email <a href="mailto:{EMAIL}?subject=Half%20Past%20alpha">{EMAIL}</a> and say if you are on iPhone or Android.</p>"""
    else:
        form = f"""<form class="formcard" action="{html.escape(SIGNUP_URL)}" method="post" accept-charset="utf-8">
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
    for slug, title, desc, body, wide in PAGES:
        with open(os.path.join(OUT, slug + ".html"), "w") as f:
            f.write(page(slug, title, desc, body, wide))
    # Pages the sign-up form returns to. Left out of the sitemap.
    extra = [
        ("thanks", "You are on the list · Half Past", "Thanks for signing up for the Half Past alpha.", THANKS, False),
        ("join-check", "Join the alpha · Half Past", "Sign up to test Half Past.",
         join_body("Something was missing or did not look right. Please check your answers and try again."), False),
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
