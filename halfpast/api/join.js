// POST /api/join: the alpha sign-up form on /join posts here.
//
// It passes the answers to the Apps Script web app behind the scenes and then
// sends the browser to /thanks or /join-check. The person never sees a Google
// page, which matters because Instagram's in-app browser shows Google's page
// as blank. The browser only ever talks to halfpast.shawlabs.dev.
//
// The script answers with one word: "ok", "check" or "error".
// Setup and the script itself: signups/SETUP.md and signups/apps-script.gs.

const SCRIPT_URL =
  "https://script.google.com/macros/s/AKfycbzoxROz9ClZnRHltlf3ayOOsTMCDVWMfjTzgoLwqnZFXb9D_wGFoIjd-_Lda_Voi-6TZA/exec";

// Only these fields are passed on, each cut to a sane length.
const FIELDS = { name: 80, email: 120, phone: 10, instagram: 40, adult: 3, emails: 3, website: 200 };
const MAX_BODY = 8 * 1024;

module.exports = async function handler(req, res) {
  if (req.method !== "POST") return go(res, "/join");

  let fields;
  try {
    fields = await readForm(req);
  } catch (err) {
    return go(res, "/join-check");
  }

  const body = new URLSearchParams();
  for (const [key, max] of Object.entries(FIELDS)) {
    body.set(key, String(fields[key] ?? "").slice(0, max));
  }

  let answer = "";
  try {
    const reply = await fetch(SCRIPT_URL, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: body.toString(),
      redirect: "follow",
      signal: AbortSignal.timeout(9000),
    });
    answer = (await reply.text()).trim();
    if (!reply.ok) answer = "error";
  } catch (err) {
    console.error("sign-up script failed", err);
    answer = "error";
  }

  if (answer === "check") return go(res, "/join-check");
  if (answer === "error") return go(res, "/join-error");
  return go(res, "/thanks");
};

function go(res, path) {
  res.statusCode = 303;
  res.setHeader("Location", path);
  res.setHeader("Cache-Control", "no-store");
  res.end();
}

// Vercel may have parsed the body already; if not, read it ourselves.
async function readForm(req) {
  if (req.body && typeof req.body === "object" && !Buffer.isBuffer(req.body)) return req.body;
  let raw = typeof req.body === "string" ? req.body : Buffer.isBuffer(req.body) ? req.body.toString("utf8") : null;
  if (raw === null) {
    raw = "";
    for await (const chunk of req) {
      raw += chunk;
      if (raw.length > MAX_BODY) throw new Error("too big");
    }
  }
  if (raw.length > MAX_BODY) throw new Error("too big");
  return Object.fromEntries(new URLSearchParams(raw));
}
