# Alpha sign-ups: setup

The form at halfpast.shawlabs.dev/join is plain HTML. It sends nothing until
someone presses Sign up. Then it posts to a Google Apps Script web app, which
checks the answers, adds a row to the sign-up sheet, emails a note to
halfpast@shawlabs.dev, and sends the person to /thanks (or /join-check if
something was missing).

## One-time setup (about 5 minutes)

1. Open the sign-up Google Sheet.
2. Extensions > Apps Script. Delete what is in `Code.gs` and paste in
   `apps-script.gs` from this folder. Save.
3. In the function menu at the top, pick `setup` and press Run. Google asks
   for permission: allow it. This makes the `Sign-ups` tab with headers and a
   Status dropdown.
4. Deploy > New deployment > gear icon > Web app.
   - Description: Half Past sign-ups
   - Execute as: Me
   - Who has access: Anyone
   Press Deploy and copy the Web app URL (it ends in `/exec`).
5. Open that URL in a browser. It should say "Half Past sign-ups are open."
6. Put the URL in `SIGNUP_URL` at the top of `halfpast/build.py`, run
   `python3 halfpast/build.py`, commit and push. Until then, /join shows the
   email route instead of the form.
7. Sign up once yourself on the live site. Check the row appears and the
   email arrives, then delete your test row.

## Changing the script later

Edit it, then Deploy > Manage deployments > pencil > Version: New version >
Deploy. The URL stays the same, so the site needs no change.

## The sheet

| Column | Filled by |
|---|---|
| Signed up, Name, Email, Phone, Instagram, 18+ confirmed, Happy to get emails | the form |
| Status | you: New, Invited, Joined, Not this round, Left |
| Notes | you |

- The same email twice adds only one row.
- Values that start with `=`, `+`, `-` or `@` are stored as text, so nobody
  can slip a formula into the sheet.
- Bots that fill the hidden field are dropped and still see /thanks.

## Formatting and the Summary tab

`setup` also runs `tidy`, which formats the sheet in the Half Past colours:
a dark header with amber text, set column widths, alternate row shading,
coloured Status values, frozen header and Name column, and filter buttons.
It also builds a Summary tab with live counts (sign-ups, iPhone and Android,
each status, last sign-up).

Run `tidy` again from the function menu whenever the sheet looks messy. It
only changes formatting, never the data. Running it needs no new deployment.

## Privacy rules this setup keeps

- The sheet is private. Do not share it.
- Use the details only for the alpha: the invite, build news, the two
  feedback forms. No marketing.
- Delete the rows when the alpha ends, except people who asked to join the
  beta. The privacy page promises this.
- If someone asks to be removed, delete their row and reply to confirm.
- Emails to testers come from halfpast@shawlabs.dev, not a personal address.
  The script only emails you; it never emails the person who signed up,
  because Apps Script would send from the account that owns it.

## Inviting people

1. Filter Status = New. Pick the next few (the alpha plan says start with five).
2. iPhone: App Store Connect > TestFlight > the Alpha external group > add
   their email. Android: Play Console > Closed testing > the tester list >
   add their email, then send them the opt-in link.
3. Email them from halfpast@shawlabs.dev with the WhatsApp group link.
4. Set Status to Invited, then Joined once they install.
