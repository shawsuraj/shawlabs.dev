/**
 * Half Past alpha sign-ups.
 *
 * Receives the plain HTML form on halfpast.shawlabs.dev/join, checks it,
 * adds one row to this sheet, emails a note to NOTIFY_EMAIL and sends the
 * person back to halfpast.shawlabs.dev/thanks.
 *
 * Setup: see halfpast/signups/SETUP.md in the shawlabs.dev repo.
 *
 * After any change to this file: Deploy > Manage deployments > edit (pencil)
 * > Version: New version > Deploy. The URL stays the same.
 */

const NOTIFY_EMAIL = 'halfpast@shawlabs.dev';
const SITE = 'https://halfpast.shawlabs.dev';
const SHEET_NAME = 'Sign-ups';
const HEADERS = [
  'Signed up', 'Name', 'Email', 'Phone', 'Instagram',
  '18+ confirmed', 'Happy to get emails', 'Status', 'Notes'
];
const STATUSES = ['New', 'Invited', 'Joined', 'Not this round', 'Left'];

/** Run once by hand. Creates the tab, headers and the Status dropdown. */
function setup() {
  const book = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = book.getSheetByName(SHEET_NAME);
  if (!sheet) sheet = book.insertSheet(SHEET_NAME);
  sheet.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]).setFontWeight('bold');
  sheet.setFrozenRows(1);
  const status = SpreadsheetApp.newDataValidation()
    .requireValueInList(STATUSES, true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange(2, HEADERS.indexOf('Status') + 1, 999, 1).setDataValidation(status);
  sheet.autoResizeColumns(1, HEADERS.length);
}

/**
 * The form posts here. A good entry goes to /thanks. A bad one goes back to
 * /join-check, except spam, which also sees /thanks so bots learn nothing.
 */
function doPost(e) {
  let next = SITE + '/thanks';
  try {
    const p = (e && e.parameter) || {};
    if (clean(p.website, 200) !== '') return back(next); // spam trap
    const entry = check(p);
    if (entry) save(entry);
    else next = SITE + '/join-check';
  } catch (err) {
    console.error(err);
    next = SITE + '/join-check';
  }
  return back(next);
}

/**
 * Sends the browser back to the site. Apps Script shows its pages in a frame,
 * so the link targets the top window, and the button works even where the
 * automatic move is blocked.
 */
function back(url) {
  const safeUrl = url.replace(/"/g, '');
  const html =
    '<!doctype html><html><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width, initial-scale=1">' +
    '<base target="_top"><title>Half Past</title></head>' +
    '<body style="margin:0;background:#2A1A10;color:#F6EBD9;font:18px/1.5 system-ui,sans-serif">' +
    '<div style="max-width:480px;margin:48px auto;padding:0 20px">' +
    '<p style="font-weight:700;font-size:22px">Thanks. Taking you back to Half Past…</p>' +
    '<p><a href="' + safeUrl + '" style="display:inline-block;background:#F5A73B;color:#2E1B0E;' +
    'font-weight:700;text-decoration:none;padding:16px 24px;border-radius:14px">Back to Half Past</a></p>' +
    '</div><script>try{window.top.location.replace("' + safeUrl + '")}catch(e){}</script>' +
    '</body></html>';
  return HtmlService.createHtmlOutput(html)
    .setTitle('Half Past')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

/** A visit in a browser shows this, so you can test the URL is live. */
function doGet() {
  return ContentService.createTextOutput('Half Past sign-ups are open.');
}

/** Returns a clean entry, or null if something is missing or wrong. */
function check(p) {

  const name = clean(p.name, 80);
  const email = clean(p.email, 120).toLowerCase();
  const phone = clean(p.phone, 10);
  const instagram = clean(p.instagram, 40).replace(/^@+/, '');
  if (!name) return null;
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return null;
  if (phone !== 'iPhone' && phone !== 'Android') return null;
  if (p.adult !== 'yes' || p.emails !== 'yes') return null;
  return { name, email, phone, instagram };
}

/** Adds the row once per email and sends the note. */
function save(entry) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    const emailCol = HEADERS.indexOf('Email') + 1;
    const last = sheet.getLastRow();
    if (last > 1) {
      const known = sheet.getRange(2, emailCol, last - 1, 1).getValues()
        .map(r => String(r[0]).toLowerCase());
      if (known.indexOf(entry.email) !== -1) return; // already signed up
    }
    sheet.appendRow([
      new Date(),
      safe(entry.name),
      safe(entry.email),
      entry.phone,
      safe(entry.instagram ? '@' + entry.instagram : ''),
      'Yes',
      'Yes',
      'New',
      ''
    ]);
  } finally {
    lock.releaseLock();
  }
  notify(entry);
}

function notify(entry) {
  const count = SpreadsheetApp.getActiveSpreadsheet()
    .getSheetByName(SHEET_NAME).getLastRow() - 1;
  const lines = [
    entry.name + ' signed up for the Half Past alpha.',
    '',
    'Email: ' + entry.email,
    'Phone: ' + entry.phone,
    'Instagram: ' + (entry.instagram ? '@' + entry.instagram : 'not given'),
    '',
    'Sign-ups so far: ' + count,
    'Sheet: ' + SpreadsheetApp.getActiveSpreadsheet().getUrl()
  ];
  MailApp.sendEmail({
    to: NOTIFY_EMAIL,
    subject: 'New Half Past sign-up: ' + entry.name + ' (' + entry.phone + ')',
    body: lines.join('\n'),
    name: 'Half Past sign-ups'
  });
}

/** Trims, caps the length and strips control characters. */
function clean(value, max) {
  return String(value == null ? '' : value)
    .replace(/[\u0000-\u001f\u007f]/g, ' ')
    .trim()
    .slice(0, max);
}

/** Stops a value being read as a sheet formula. */
function safe(value) {
  return /^[=+\-@]/.test(value) ? "'" + value : value;
}
