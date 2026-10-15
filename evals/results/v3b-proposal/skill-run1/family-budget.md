# family-budget (skill)

**Persona:** You and your wife want to see where your money goes each month. You're not technical. You both use iPhones. You'd want to add expenses quickly and see a monthly total by category. You're a bit worried about privacy since it's your finances. Short messages.

## Turn 1

**User:** /vibe can you build something so me and my wife can track our spending together

`[tool] Bash {"command": "ls -la <workdir> 2>&1 | head -30 && echo \"---\" && ls -la <workdir> 2>&1", "description": "Check working directory and vibe profile"}`

`[tool] Read {"file_path": "<workdir>"}`

Happy to build this with you. A shared spending tracker can mean a few different things, and which one you pick changes the whole thing — so let me start there.

`[tool] AskUserQuestion {"questions": [{"question": "When you say \"track spending together\", which of these fits best?", "header": "Tracker type", "multiSelect": false, "options": [{"label": "Shared expense log", "description": "Both of you add what you spent (groceries, gas, rent), everything shows up in one list you can both see. Good for: knowing where the money is going as a household. (my pick to start \u2014 simp`

Happy to build this with you. "Track spending together" can mean a few different things, and the one you pick shapes the whole thing — so let me start there.

**Which of these fits best?**

a. **Shared expense log**: both of you add what you spent (groceries, gas, rent), it all shows up in one list you can both see. Good for knowing where the money is going as a household. *(my pick to start — simplest, and it's what most couples I've built this for actually wanted)*

b. **Budget vs. actual**: you set monthly limits per category (eating out, groceries, etc.) and watch how much is left.

c. **Who-owes-who split**: like Splitwise — you log who paid, it tracks who owes the other for shared stuff. Good if your money is still separate and you settle up each month.

d. **All three**: log + budgets + splitting. Bigger, so we'd build the log first and add the rest in stages.

_words: 192 · questions: 1 · files changed: 0 _

## Turn 2

**User:** A sounds right — we just want to see where it's going. And can you keep it private? I don't love the idea of our money stuff sitting on some server.

Got it — a shared log of what you two spend. That matters.

Here's the honest bit about privacy: for both of you to see the same list from two different phones, the data has to live somewhere you can both reach. There's no way around that. What **is** in your control is **whose account that place lives in**, and whether anyone else could read it.

Two realistic ways to do this:

a. **A shared spreadsheet in your own Google Drive** (**spreadsheet** = like Excel, but online). The list lives inside your Google account, which you already have. You share it with your wife with a link, nobody else gets in. Google itself can technically see your Drive files like with any other Drive file. Zero setup from you beyond the share. *(my pick for easy and private-enough — most couples I've seen stop here)*

b. **A tiny private database only you two can read.** You'd make a free account on **Supabase** (a service that hosts little databases for apps like this), paste two values into a settings file, and I'd lock it so only you two can read or write. Nobody else — not Google, not me, not Supabase staff poking around casually. Still free. Costs you one 5-minute signup.

Which feels right?

_words: 214 · questions: 1 · files changed: 0 _

## Turn 3

**User:** Let's go with the spreadsheet, keep it simple.

Spreadsheet it is. Your Google account, your data.

One more thing to settle before I pitch the whole picture: **how do you want to add an expense on the go?**

a. **Just open the Google Sheet on your phone and tap a row.** No app, no page, nothing to build beyond laying the sheet out well with categories, totals, maybe a little chart. Google Sheets has a phone app you both already have. Simplest. ← fits "keep it simple" best

b. **A small web page that saves into the sheet.** You open a link, big "Add" button, type amount, pick category, done — much faster than tapping tiny cells on a phone. The sheet still holds everything (and does the totals and charts); the page is just a friendlier front door. Takes a bit more to set up but it's the thing that feels like *an app* rather than homework.

Which way? (I lean b because adding things on a phone in Sheets is painful — but a is a totally fine answer.)

_words: 173 · questions: 1 · files changed: 0 _

## Turn 4

**User:** let's go with b, tapping cells on the phone sounds annoying. just make sure only me and my wife can see it.

Done. Let me pitch the whole picture before we start.

**How it'll work when it's done:**
1. You open a bookmark on your phone. First time, you sign in with Google. After that, straight in.
2. Big "Add" button → type the amount, pick a category, hit save. Five seconds.
3. Below that: recent entries, newest first. Tap one to edit or delete.
4. Up top: how much the two of you have spent this month.
5. Your wife opens the same link on her phone, signs in as her, and sees the same list. Her entries appear on your phone, yours on hers.

**What's in front, what's behind:**
- **What you see** (the front end): the one page above, built to work on a phone.
- **Behind the scenes** (the back end): your private Google Sheet (shared only with you two) + a small script attached to it (**Google Apps Script** — a way to add code to a Google Sheet). The script serves the page *and* refuses anyone who isn't signed in as one of your two Google accounts. So even if the link leaked, nobody else could get in. Google itself hosts the whole thing — no second service, no fees.

**Features I'd suggest** (pick any, or none):

- **Categories with a drop-down** (groceries, eating out, gas, bills, etc.): otherwise "where it's going" doesn't actually tell you anything. *(I'd do this one first — it's the point of the whole thing)*
- **A little this-month-by-category bar chart**: see at a glance what's eating the money.
- **Who added it**: your name or hers on each row. Nice-to-see.
- **"Common ones" quick buttons** (e.g. tap "Coffee $5" instead of typing): speeds up the daily small stuff.

Which of these do you want?

_words: 294 · questions: 1 · files changed: 0 _

## Turn 5

**User:** Categories for sure, and the bar chart. Skip the rest for now — keep it simple.

Here's how I'd build it, in 5 small steps:

1. **Create and set up the sheet** — you make a new Google Sheet, share it with just your wife, and I give you the exact column names to drop in. ← we start here
2. **The basic app: Add + recent list** — I write a script; you paste it into the sheet and click "Deploy". You get a URL that already works. At this point anyone with the URL could use it; we fix that in step 3.
3. **Lock it to just you two** — I update the script so only your two Google accounts are let in. Everyone else gets "Access denied."
4. **Categories drop-down + monthly total up top.**
5. **The bar chart (this month by category).**

**Why this way:** step 2 proves the plumbing works so if something breaks later we know where. Step 3 is the privacy step — I'll be explicit when we're there. Steps 4–5 are the parts that make it actually useful.

**Worth knowing:**
- Nothing costs money. Google's free tier covers two people easily.
- I'll never see your Google password. For step 3 I'll ask for the two Google emails (not passwords) that should be let in.
- Between steps 2 and 3, the URL will be live. Don't share it until step 3 is done.

Start with step 1?

_words: 231 · questions: 1 · files changed: 0 _

## Turn 6

**User:** Yeah let's start. What do I do first?

**Step 1: Make the sheet.**

Easier on a computer than a phone. On your computer:

1. Go to **sheets.google.com** and click the big "+" (Blank spreadsheet).
2. At the top, click where it says **Untitled spreadsheet** and name it **Our Spending** (or whatever).
3. In the very first row (row 1), type these four column headers, one per cell:
   - `A1: Date`
   - `B1: Amount`
   - `C1: Category`
   - `D1: Note`
4. Click the green **Share** button (top right), type your wife's Google email, make sure the dropdown says **Editor**, send. She'll get an email with the sheet. Only she and you have access — nobody else.
5. Add one or two sample rows by hand so step 2 has something to show. E.g.:
   - `2026-10-14 | 12.50 | Groceries | coffee beans`
   - `2026-10-15 | 48.00 | Gas | Costco fill-up`

**Try it:** scroll around, type in a row, change a number. This sheet **is** the whole database — every expense you'll ever add through the app will end up here as a row. If something ever looks wrong in the app, you can open the sheet and see exactly what's stored. Nothing hidden.

**The idea:** by putting your data in a Google Sheet instead of some new place, you keep ownership of it. If one day you don't want the app anymore, the sheet is still yours with all the data in it.

**Ready for step 2?** When you are, paste the sheet's URL (the thing in your browser's address bar) here — I'll need it to write the script in step 2.

_words: 265 · questions: 1 · files changed: 0 _

## Turn 7

**User:** ok did it. shared with my wife, added a couple rows. here's the link: https://docs.google.com/spreadsheets/d/1a2b3c4d5e6f7g8h9i0j/edit

ready for step 2

**Step 2: The script, deployed as an app.**

Heads up — this is the longest step. After this it gets easier.

**Small change from the plan:** instead of "anyone with the URL", I'm starting with **only you** having access. Safer, same amount of work. Your wife joins in step 3.

**In your sheet, do this:**

1. Click **Extensions → Apps Script**. A new tab opens with a code editor.
2. You'll see a file `Code.gs` with some starter code. Select all (⌘A / Ctrl+A), delete, and paste the **Code.gs** block below.
3. On the left panel, click the **+** next to "Files" → **HTML**. Name it exactly `Index` (capital I). It'll open with starter content — delete that, paste the **Index.html** block below.
4. Click the floppy-disk save icon (⌘S / Ctrl+S).
5. Click **Deploy** (top right) → **New deployment** → click the gear next to "Select type" → **Web app**.
6. Fill in:
   - **Description:** `spending v1` (anything, doesn't matter)
   - **Execute as:** Me
   - **Who has access:** **Only myself**
7. Click **Deploy**. Google will ask you to authorize — click **Authorize access**, pick your account, you may see a "Google hasn't verified this app" warning (because *you* made it, so Google hasn't). Click **Advanced → Go to [project name] (unsafe)**. It's your own script; the warning is for when apps come from strangers.
8. Copy the **Web app URL** it shows you. That's your app.

**Code.gs:**
```js
function sheet_() {
  return SpreadsheetApp.getActive().getSheets()[0];
}

function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('Our Spending')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function addExpense(data) {
  const s = sheet_();
  const date = data.date || new Date().toISOString().slice(0, 10);
  const amount = Number(data.amount) || 0;
  const category = (data.category || '').trim();
  const note = (data.note || '').trim();
  s.appendRow([date, amount, category, note]);
  return { ok: true };
}

function getRecent(limit) {
  const s = sheet_();
  const lastRow = s.getLastRow();
  if (lastRow < 2) return [];
  const n = Math.min(limit || 20, lastRow - 1);
  const rows = s.getRange(lastRow - n + 1, 1, n, 4).getValues();
  const tz = Session.getScriptTimeZone();
  return rows.reverse().map((r) => ({
    date: r[0] instanceof Date ? Utilities.formatDate(r[0], tz, 'yyyy-MM-dd') : String(r[0]),
    amount: r[1],
    category: r[2],
    note: r[3],
  }));
}
```

**Index.html:**
```html
<!DOCTYPE html>
<html>
<head>
  <base target="_top">
  <style>
    body { font-family: -apple-system, system-ui, sans-serif; max-width: 480px; margin: 0 auto; padding: 16px; color: #222; }
    h1 { font-size: 20px; margin: 8px 0 16px; }
    h2 { font-size: 15px; color: #555; margin: 24px 0 8px; }
    form { display: grid; gap: 10px; }
    input { padding: 12px; font-size: 16px; border: 1px solid #ccc; border-radius: 8px; width: 100%; box-sizing: border-box; }
    button { padding: 14px; font-size: 16px; background: #2c7a5a; color: #fff; border: 0; border-radius: 8px; }
    button:disabled { opacity: .5; }
    .row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }
    .meta { color: #777; font-size: 13px; }
    .amount { font-weight: 600; }
    #status { color: #2c7a5a; font-size: 14px; min-height: 20px; }
  </style>
</head>
<body>
  <h1>Our Spending</h1>
  <form id="f">
    <input type="date" id="date" required>
    <input type="number" inputmode="decimal" step="0.01" id="amount" placeholder="Amount" required>
    <input type="text" id="category" placeholder="Category (e.g. Groceries)" required>
    <input type="text" id="note" placeholder="Note (optional)">
    <button type="submit" id="submit">Add</button>
    <div id="status"></div>
  </form>
  <h2>Recent</h2>
  <div id="list">Loading…</div>
  <script>
    const dateEl = document.getElementById('date');
    dateEl.value = new Date().toISOString().slice(0, 10);

    document.getElementById('f').addEventListener('submit', (e) => {
      e.preventDefault();
      const btn = document.getElementById('submit');
      btn.disabled = true;
      document.getElementById('status').textContent = 'Saving…';
      const data = {
        date: dateEl.value,
        amount: document.getElementById('amount').value,
        category: document.getElementById('category').value,
        note: document.getElementById('note').value,
      };
      google.script.run
        .withSuccessHandler(() => {
          document.getElementById('status').textContent = 'Saved';
          document.getElementById('amount').value = '';
          document.getElementById('note').value = '';
          btn.disabled = false;
          loadRecent();
          setTimeout(() => document.getElementById('status').textContent = '', 1500);
        })
        .withFailureHandler((err) => {
          document.getElementById('status').textContent = 'Error: ' + err.message;
          btn.disabled = false;
        })
        .addExpense(data);
    });

    function loadRecent() {
      google.script.run
        .withSuccessHandler((rows) => {
          const list = document.getElementById('list');
          if (!rows.length) { list.textContent = 'No entries yet.'; return; }
          list.innerHTML = rows.map((r) => `
            <div class="row">
              <div>
                <div>${r.category || '(uncategorised)'}</div>
                <div class="meta">${r.date}${r.note ? ' · ' + r.note : ''}</div>
              </div>
              <div class="amount">$${Number(r.amount).toFixed(2)}</div>
            </div>`).join('');
        })
        .getRecent(20);
    }
    loadRecent();
  </script>
</body>
</html>
```

**Try it:** open the Web app URL (on your phone or computer, signed into the same Google account that owns the sheet). You should see your two sample rows at the bottom. Add one through the form — it should pop into the list, and if you flip to your sheet tab you'll see the row there too.

**The idea:** two parts, talking. The page in your browser is the **front end**. The script inside the sheet is the **back end** (= code running on Google's computers, not your phone, that touches the data). The front end never writes to the sheet directly — it asks the back end "please add this row", and the back end does it. That split is the whole reason step 3 is easy: all requests go through the back end, so one check there blocks everyone we don't want.

**If something breaks:** tell me what you see (the exact error message, or "the page is blank", etc.). Don't share the URL yet — only you can get in right now anyway.

**For step 3, reply with:**
- Your Google email (the one you used to make the sheet)
- Your wife's Google email

I'll never ask for passwords.

_words: 443 · questions: 1 · files changed: 0 _

## Turn 8

**User:** ok did all that. added a coffee for $4 and it showed up in the list and in the sheet. worked on my phone too.

my email is aiintracter@gmail.com, wife's is sarah.k.harper@gmail.com

one thing — you said only i can get in, but the sheet itself, can she see that too or no? just want to make sure our stuff stays between us.

Good question. Here's who sees what right now:

- **The sheet**: just you and your wife. You shared it with her in step 1 — she can open it in Google Sheets right now by herself. Nobody else.
- **The app (right now)**: only you. "Only myself" means literally that. Even your wife can't open the URL yet — we're about to fix that.
- **Google itself**: as the host, it can technically see your Drive files like any Drive file. No other person, no other company.

Nothing is "on a stranger's server". It all lives inside your Google account.

---

**Step 3: Let your wife in, keep everyone else out.**

Two parts: a code change and a deployment change.

**Code change — in Apps Script, open Code.gs, select all, delete, paste this whole thing:**

```js
const ALLOWED = [
  'aiintracter@gmail.com',
  'sarah.k.harper@gmail.com',
];

function authorized_() {
  const email = (Session.getActiveUser().getEmail() || '').toLowerCase();
  return email && ALLOWED.map((e) => e.toLowerCase()).includes(email);
}

function sheet_() {
  return SpreadsheetApp.getActive().getSheets()[0];
}

function doGet() {
  if (!authorized_()) {
    return HtmlService.createHtmlOutput(
      '<div style="font-family:-apple-system,system-ui,sans-serif;padding:40px;text-align:center;color:#555;">' +
      '<h2>Access denied</h2><p>This app is private.</p></div>'
    ).setTitle('Access denied');
  }
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('Our Spending')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function addExpense(data) {
  if (!authorized_()) throw new Error('Not authorized');
  const s = sheet_();
  const date = data.date || new Date().toISOString().slice(0, 10);
  const amount = Number(data.amount) || 0;
  const category = (data.category || '').trim();
  const note = (data.note || '').trim();
  s.appendRow([date, amount, category, note]);
  return { ok: true };
}

function getRecent(limit) {
  if (!authorized_()) throw new Error('Not authorized');
  const s = sheet_();
  const lastRow = s.getLastRow();
  if (lastRow < 2) return [];
  const n = Math.min(limit || 20, lastRow - 1);
  const rows = s.getRange(lastRow - n + 1, 1, n, 4).getValues();
  const tz = Session.getScriptTimeZone();
  return rows.reverse().map((r) => ({
    date: r[0] instanceof Date ? Utilities.formatDate(r[0], tz, 'yyyy-MM-dd') : String(r[0]),
    amount: r[1],
    category: r[2],
    note: r[3],
  }));
}
```

Save (⌘S / Ctrl+S). `Index.html` doesn't change.

**Deployment change:**

1. Click **Deploy → Manage deployments**.
2. Click the pencil (edit) icon next to your existing deployment.
3. **Version:** New version.
4. **Execute as:** change to **User accessing the web app**.
5. **Who has access:** change to **Anyone with Google account**.
6. Click **Deploy**. The URL stays the same.

*If "Execute as" is greyed out:* click Cancel, then **Deploy → New deployment** (gear → Web app), use those two settings, deploy. You'll get a **new URL** — that's the real one now; stop using the old one.

**Try it (do these in order):**

- Open the URL yourself first. Looks the same? Good.
- Temporarily change one of the emails in `ALLOWED` to something wrong (e.g. put an `x` on the end of yours), save, redeploy "New version", reload the page. You should see **Access denied**. That's proof the lock works. Fix the email back, save, redeploy, reload — you're back in.
- Now send the URL to your wife. First time she opens it she'll see Google's "this app isn't verified" warning — tell her it's your app, click **Advanced → Go to [project name] (unsafe)**, then **Allow**. She'll be in. Her entries will show up on your phone, yours on hers.

**The idea:** two layers protect you now. **One**: the sheet is shared with only you two, so Google itself refuses to let anyone else read or write it. **Two**: the `ALLOWED` list in the script locks the front door and shows a clean "Access denied" page to anyone who tries. If one day you want to add someone (an accountant, a parent), just add their email to that list.

**One honest note on security:** this is "as safe as your Google accounts". If your Google password leaked, someone could get in. Same as your Gmail or Drive. Use 2-step verification on both accounts if you don't already — that's the one thing worth doing today.

**Next (step 4):** categories drop-down + "spent this month" total up top. Smaller step. Ready?

_words: 477 · questions: 2 · files changed: 0 _

## Metrics

| Turn | Words | Questions | Files changed | Proposal |
|---|---|---|---|---|
| 1 | 192 | 1 | 0 |  |
| 2 | 214 | 1 | 0 |  |
| 3 | 173 | 1 | 0 |  |
| 4 | 294 | 1 | 0 | yes |
| 5 | 231 | 1 | 0 |  |
| 6 | 265 | 1 | 0 |  |
| 7 | 443 | 1 | 0 |  |
| 8 | 477 | 2 | 0 |  |

- Turns: 8
- First file change on turn: None
- Most files changed in one turn: 0
- Proposal (how it works, front/back, suggested features) on turn: 4 (before first code change)
- Turns asking more than one question: 1
- Turns ending with no question: 0
- Average words per turn: 286
