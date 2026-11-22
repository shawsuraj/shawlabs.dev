/**
 * Half Past alpha sign-ups.
 *
 * The form on halfpast.shawlabs.dev/join posts to the site's /api/join,
 * which passes it on to here. This checks it, adds one row to this sheet,
 * emails a note to NOTIFY_EMAIL and answers with one word.
 *
 * Setup: see halfpast/signups/SETUP.md in the shawlabs.dev repo.
 *
 * After any change to this file: Deploy > Manage deployments > edit (pencil)
 * > Version: New version > Deploy. The URL stays the same.
 */

const NOTIFY_EMAIL = 'halfpast@shawlabs.dev';
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
  sheet.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
  tidy();
}

// Half Past colours, from the site.
const DARK = '#2A1A10';
const AMBER = '#F5A73B';
const CREAM = '#FBF5EC';
const STATUS_COLOURS = {
  'New':            ['#FCE6C4', '#7A4A0E'],
  'Invited':        ['#DCE8F8', '#1F4E8C'],
  'Joined':         ['#DDF0DC', '#1E6B2E'],
  'Not this round': ['#ECECEC', '#666666'],
  'Left':           ['#F8DCDC', '#9B2C2C']
};
// Column widths in pixels, in the order of HEADERS.
const WIDTHS = [140, 160, 240, 90, 140, 70, 70, 120, 300];

/**
 * Formats the Sign-ups tab and builds the Summary tab. Safe to run again
 * any time the sheet looks messy. It never changes the data.
 */
function tidy() {
  const book = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = book.getSheetByName(SHEET_NAME);
  const cols = HEADERS.length;
  const rows = sheet.getMaxRows();
  const col = name => HEADERS.indexOf(name) + 1;

  // Shorter labels for the two narrow tick columns.
  const labels = HEADERS.slice();
  labels[col('18+ confirmed') - 1] = '18+';
  labels[col('Happy to get emails') - 1] = 'Emails ok';
  sheet.getRange(1, 1, 1, cols).setValues([labels]);

  // Whole sheet: font, height, vertical centring.
  const all = sheet.getRange(1, 1, rows, cols);
  all.setFontFamily('Arial').setFontSize(10).setVerticalAlignment('middle')
     .setWrap(false);
  sheet.setRowHeights(2, rows - 1, 28);
  sheet.setHiddenGridlines(true);

  // Header.
  sheet.getRange(1, 1, 1, cols)
    .setBackground(DARK).setFontColor(AMBER).setFontWeight('bold')
    .setFontSize(11).setHorizontalAlignment('left');
  sheet.setRowHeight(1, 38);
  sheet.setFrozenRows(1);
  sheet.setFrozenColumns(col('Name'));

  // Widths.
  WIDTHS.forEach((w, i) => sheet.setColumnWidth(i + 1, w));

  // Per column formats.
  const body = (name) => sheet.getRange(2, col(name), rows - 1, 1);
  body('Signed up').setNumberFormat('d mmm, HH:mm').setFontColor('#6B5B4E');
  body('Name').setFontWeight('bold');
  ['Phone', '18+ confirmed', 'Happy to get emails']
    .forEach(n => body(n).setHorizontalAlignment('center'));
  ['18+ confirmed', 'Happy to get emails']
    .forEach(n => body(n).setFontColor('#1E6B2E'));
  body('Notes').setWrap(true);
  body('Status').setHorizontalAlignment('center').setFontWeight('bold');

  // Status dropdown.
  const rule = SpreadsheetApp.newDataValidation()
    .requireValueInList(STATUSES, true)
    .setAllowInvalid(false)
    .build();
  body('Status').setDataValidation(rule);

  // Alternate row shading, header included in the band.
  sheet.getBandings().forEach(b => b.remove());
  all.applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY, true, false)
    .setHeaderRowColor(DARK)
    .setFirstRowColor('#FFFFFF')
    .setSecondRowColor(CREAM);

  // Status colours, which sit on top of the shading.
  const statusRange = body('Status');
  const kept = sheet.getConditionalFormatRules().filter(r =>
    !r.getRanges().some(g => g.getColumn() === col('Status')));
  const statusRules = Object.keys(STATUS_COLOURS).map(s =>
    SpreadsheetApp.newConditionalFormatRule()
      .whenTextEqualTo(s)
      .setBackground(STATUS_COLOURS[s][0])
      .setFontColor(STATUS_COLOURS[s][1])
      .setRanges([statusRange])
      .build());
  sheet.setConditionalFormatRules(kept.concat(statusRules));

  // Filter buttons on the header.
  if (sheet.getFilter()) sheet.getFilter().remove();
  all.createFilter();

  summary(book);
}

/** A small Summary tab with live counts. */
function summary(book) {
  let s = book.getSheetByName('Summary');
  if (!s) s = book.insertSheet('Summary');
  s.clear();
  const src = "'" + SHEET_NAME + "'!";
  const rows = [
    ['Half Past alpha', ''],
    ['', ''],
    ['Sign-ups', '=COUNTA(' + src + 'C2:C)'],
    ['iPhone', '=COUNTIF(' + src + 'D2:D,"iPhone")'],
    ['Android', '=COUNTIF(' + src + 'D2:D,"Android")'],
    ['', ''],
    ['Status', '']
  ].concat(STATUSES.map(st => [st, '=COUNTIF(' + src + 'H2:H,"' + st + '")']))
   .concat([['', ''], ['Last sign-up', '=IFERROR(MAX(' + src + 'A2:A),"")']]);
  s.getRange(1, 1, rows.length, 2).setValues(rows);

  s.setHiddenGridlines(true);
  s.setColumnWidth(1, 160);
  s.setColumnWidth(2, 140);
  s.getRange(1, 1, rows.length, 2).setFontFamily('Arial').setFontSize(11)
    .setVerticalAlignment('middle');
  s.setRowHeights(1, rows.length, 28);
  s.getRange(1, 1, 1, 2).merge().setBackground(DARK).setFontColor(AMBER)
    .setFontWeight('bold').setFontSize(14);
  s.setRowHeight(1, 40);
  s.getRange(3, 1, 1, 2).setFontWeight('bold').setFontSize(13);
  s.getRange(7, 1).setFontWeight('bold').setFontColor('#6B5B4E');
  s.getRange(3, 2, rows.length - 2, 1).setHorizontalAlignment('right');
  STATUSES.forEach((st, i) => s.getRange(8 + i, 1)
    .setBackground(STATUS_COLOURS[st][0]).setFontColor(STATUS_COLOURS[st][1])
    .setFontWeight('bold'));
  s.getRange(rows.length, 2).setNumberFormat('d mmm, HH:mm');
}

/**
 * The site's /api/join passes the form on to here and reads the answer:
 * "ok" (saved, or already on the list), "check" (something missing or wrong)
 * or "error". Spam also gets "ok", so bots learn nothing.
 */
function doPost(e) {
  try {
    const p = (e && e.parameter) || {};
    if (clean(p.website, 200) !== '') return reply('ok'); // spam trap
    const entry = check(p);
    if (!entry) return reply('check');
    save(entry);
    return reply('ok');
  } catch (err) {
    console.error(err);
    return reply('error');
  }
}

function reply(word) {
  return ContentService.createTextOutput(word).setMimeType(ContentService.MimeType.TEXT);
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
