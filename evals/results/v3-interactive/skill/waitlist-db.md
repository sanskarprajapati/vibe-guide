# waitlist-db (skill)

**Persona:** You run a small side project called Plantpal and made this waitlist page with AI help last week. You're not technical. You want to collect emails before launch and look at the list. Budget is small. You'd rather not share any passwords or keys with the AI.

## Turn 1

**User:** /vibe add a database to store the signups

`[tool] Bash {"command": "ls -la <workdir>", "description": "List project directory contents"}`

`[tool] Bash {"command": "ls -la <workdir> 2>/dev/null; ls -la <workdir>", "description": "Check vibe profile and app directory"}`

I'll start the vibe conversation. Let me peek at the current app to see what we're working with.

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Bash {"command": "ls <workdir> && cat <workdir> 2>/dev/null; cat <workdir>", "description": "Peek at signup API route and package.json"}`

Right now your signup page takes an email and… throws it away. The API prints it to a log that disappears as soon as the app restarts. So before I wire anything up, the one thing we need to decide is **where the emails should live**.

A few real options, each with a real trade-off:

- **Google Sheet** — every signup appears as a new row in a spreadsheet you own. You can see them, sort them, export them. Easiest to look at, but a bit hacky for scale.
- **Supabase** — a hosted database (a filing cabinet in the cloud) with a free tier and a dashboard where you can see rows. Standard pick for small sites, free up to ~500MB. Needs a quick account signup.
- **A plain text file on the server** — simplest to write, but on most modern hosts (Vercel, Netlify) the file gets wiped on every deploy. Fine for local tinkering, not for a real waitlist.

My recommendation: **Supabase**. It's free, survives deploys, and you'll get a dashboard that shows "here are the people who signed up" without me building one. The only cost is a 2-minute account signup.

One heads-up before we pick: whatever we choose will eventually hold real people's email addresses, so we'll need to keep its keys out of git. I'll handle that when we get there.

Which one feels right — Supabase, Google Sheet, or something else?

_words: 256 · questions: 1 · files changed: 0 _

## Turn 2

**User:** Supabase sounds good but I'm a little nervous about the keys thing — I don't really want to hand you any passwords. Can we do it in a way where I set up the account myself and you just tell me what to paste where?

Yes — that's exactly how we should do it, and honestly it's the right instinct. I never need to see your keys, and I shouldn't. The way it works:

- **You** make the Supabase account, create the project, and create the table.
- **Supabase** gives you two values on their dashboard: a **project URL** (the address of your database) and an **API key** (a long string that proves requests are coming from your app).
- **You** paste those two values into a file called `.env.local` in your project. That file stays on your computer — it never gets committed to git, and I never need to see what's inside it.
- **I** write the code that reads those values by name (`process.env.SUPABASE_URL`, etc.), so the code works without me ever knowing the actual values.

Let me save that preference so I don't forget it later.

`[tool] Write {"file_path": "~/.claude/projects/-private-var-folders-0j-jc0c5qw572z1qpb9y9ngtlvc0000gn-T-public-waitlist-6r804by4/memory/feedback_credentials.md", "content": "---\nname: feedback-credentials\ndescription: User sets up third-party accounts themselves and pastes keys into local env files; never share keys in chat\nmetadata:\n  type: feedback\n---\n\nUser wants to handle account creati`

`[tool] Write {"file_path": "~/.claude/projects/-private-var-folders-0j-jc0c5qw572z1qpb9y9ngtlvc0000gn-T-public-waitlist-6r804by4/memory/MEMORY.md", "content": "- [Credentials handling](feedback_credentials.md) \u2014 user creates accounts themselves and pastes keys into local env files; never ask for keys in chat\n"}`

Here's how I'd do it, in 4 small steps:

1. **You** sign up at supabase.com and create a new project (I'll walk you through what to click). ← we start here
2. **You** make a `signups` table with two columns: `email` and `created_at`.
3. **You** copy the URL + key into `.env.local`. I write the code that reads them.
4. **I** update the signup API to save emails to the database. We test it together.

Ready for step 1? If so, open [supabase.com](https://supabase.com) and tell me when you've created a free account — I'll guide you through creating the project from there.

_words: 247 · questions: 1 · files changed: 0 _

## Turn 3

**User:** Ok I'm on supabase.com now, I signed up with my google account. What do I click next?

Nice. You should see a dashboard, and somewhere near the top there'll be a green **"New project"** button (or "Create a new project"). Click that.

It'll show you a short form. Here's what to put:

- **Name** — something like `plantpal-waitlist`. This is just a label you'll see on your own dashboard.
- **Database Password** — it'll suggest a strong random one. **Save this somewhere** (a password manager, or a note on your computer). I won't need it, but if you ever want to poke at the database directly, you will. If you lose it you can reset it later, so it's not catastrophic.
- **Region** — pick whichever is closest to you (e.g. "West US", "Europe (Frankfurt)"). This affects speed, nothing else.
- Leave anything else at its default.

Then hit **"Create new project"**. Supabase will spin it up — takes about a minute. You'll see a loading screen with a "Setting up project…" message.

Let me know when it's done and you're looking at the project dashboard, and we'll make the table.

_words: 174 · questions: 0 · files changed: 0 _

## Turn 4

**User:** Ok done, named it plantpal-waitlist and saved the password in my notes. It's showing me the project dashboard now.

On the left side of the dashboard there's a sidebar with icons. Find the one that looks like a little grid/table — it's called **Table Editor** (if you hover, it'll say "Table Editor"). Click that.

You'll see a mostly empty page with a green **"New table"** button. Click that. A side panel will slide out. Fill it in like this:

- **Name**: `signups`
- **Description**: leave blank
- **Enable Row Level Security (RLS)**: leave this **checked** (it's on by default). (A **table** is like a spreadsheet with named columns; **row-level security** is a lock that says "only requests with a trusted key can write here" — we want that.)

Scroll down to **Columns**. Supabase will already have given you two for free: `id` (a unique number per row) and `created_at` (a timestamp of when the row was added). Below those, click **"+ Add column"** and set:

- **Name**: `email`
- **Type**: `text`
- Check the box labelled **"Is Nullable"**… actually, **uncheck** it. (We don't want rows without an email — "not nullable" means "this field is required".)
- Leave Default Value blank.

Then click **Save** at the bottom.

One thing I'm picking for you without asking: I'm not adding a "unique" constraint on email yet, so the same person could technically sign up twice. If that becomes annoying, we can add it in a minute. Just flagging it.

Let me know when the table shows up (you should see it listed in the sidebar on the left under your project).

_words: 250 · questions: 0 · files changed: 0 _

## Turn 5

**User:** Ok done, I see "signups" in the sidebar now. The duplicate email thing is fine for now, we can fix it later if it gets annoying.

Great. Now we grab the two values the code needs.

In the sidebar, find the **gear icon** (⚙️) near the bottom-left — that's **Project Settings**. Click it, then click **API** (or **API Keys** / **Data API** depending on your Supabase version) in the submenu that appears.

You'll see two things we want:

1. **Project URL** — looks like `https://xxxxxxxxxx.supabase.co`. Copy that.
2. Scroll down to **Project API keys** (or just "API keys"). You'll see two keys listed: `anon` (public) and `service_role` (secret). We want the **`service_role`** one — it'll be hidden behind a "Reveal" button. Click reveal, then copy it.

Quick note on what these are: the **URL** is the address of your database. The **service_role key** is a password that proves our server is allowed to write. Because it's powerful (anyone with it can read/write anything in your DB), we only ever use it from the server side — never in browser code — and we keep it in a file that never goes to git. More on that in a sec.

Now, in your project folder (`<workdir>`), create a new file called **`.env.local`** at the top level (same place as `package.json`). Paste this in, replacing the placeholders with the values you just copied:

```
SUPABASE_URL=https://xxxxxxxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=paste-the-long-service_role-key-here
```

Save it. I'll create a `.gitignore` on my side so if you ever turn this into a git repo later, this file is automatically kept out.

`[tool] Write {"file_path": "<workdir>", "content": "node_modules\n.next\n.env*.local\n"}`

Done on my side. Tell me when you've saved `.env.local` with your two values and we'll wire the signup API up to actually store rows.

_words: 256 · questions: 1 · files changed: 1 ['.gitignore']_

## Turn 6

**User:** Hold on — you said earlier you wouldn't need my passwords or keys, but the service_role one sounds like a password to the database. I'd rather not paste that into a chat with you. Is there a way to do this where I keep that key to myself?

You're right to push on this, and let me clear up what I meant and offer a better path.

**First, a clarification.** `.env.local` lives on your computer — not in this chat. When I said "paste it in `.env.local`", I never meant "send it to me". My code reads it by *name* (`process.env.SUPABASE_SERVICE_ROLE_KEY`), not by value. I never see the string.

**But — your deeper instinct is still valid.** I technically have a file-reading tool, so "it's just on your computer" isn't an airtight promise. I won't read that file, but a stronger answer is: let's not even make that trust necessary.

So let's switch approach. Supabase gives you two keys:
- **`service_role`** — a master key (what I asked for). Powerful, should stay secret.
- **`anon`** — a public key, **designed to be shared**. Supabase apps literally ship this one in browser code. On its own, it can't do anything the table doesn't explicitly allow.

If we use the `anon` key and add one rule to your `signups` table that says "only inserts are allowed", then even if that key appeared on a billboard, the worst anyone could do is add a signup — same as filling out your form. The powerful key stays inside Supabase, never leaving.

That matches your instinct way better. It's one extra click in Supabase (adding the rule) but genuinely safer.

Want to switch to that? If yes, delete the `.env.local` you just made (or clear it), and I'll walk you through the new path.

_words: 251 · questions: 1 · files changed: 0 _

## Turn 7

**User:** Yes let's switch to that, I like that way better. I deleted what I put in the file. What do I do next?

Let me update that preference note so I don't need you to re-explain next time.

`[tool] Edit {"replace_all": false, "file_path": "~/.claude/projects/-private-var-folders-0j-jc0c5qw572z1qpb9y9ngtlvc0000gn-T-public-waitlist-6r804by4/memory/feedback_credentials.md", "old_string": "User wants to handle account creation and credentials themselves \u2014 I should guide them to the dashboard, tell them exactly what to paste into `.env.local` (or similar), and write code that reads v`

OK. Here's the plan: first we add the "only inserts allowed" rule to your table, then we grab the public key. Let's do the rule first.

In the sidebar, click **Table Editor**, then click your **signups** table. At the top of the table view, you'll see a banner or badge that says something like **"Row Level Security is enabled"** with a note that no policies exist (which means right now, *nothing* can read or write — we need to add a policy).

Click **"Add RLS policy"** (or the "Policies" link / tab, depending on your UI version). You'll land on a Policies page for the `signups` table. Click **"New policy"** (or **"Create policy"**).

You'll usually get a choice between **"Get started quickly" (templates)** and **"For full customization"**. Pick **"For full customization"** — easier to be sure what's happening. Fill it in like this:

- **Name**: `Allow public inserts`
- **Allowed operation**: check **INSERT** only (uncheck SELECT, UPDATE, DELETE if those are checked)
- **Target roles**: leave blank, OR select `anon` and `authenticated` if it asks. (Blank means "anyone".)
- **WITH CHECK expression**: type exactly `true` (the word `true`, no quotes). This means "any insert that comes in is allowed".
- Leave **USING expression** blank (it only applies to reads/updates/deletes).

Then click **Review** → **Save policy**.

What this does in plain words: it tells the database "the anon key is allowed to add new signup rows, but can't read, change, or delete anything". That's the structural lock that makes the anon key safe to use.

Tell me when the policy shows up in the list, and we'll grab the anon key.

_words: 285 · questions: 0 · files changed: 0 _

## Turn 8

**User:** Ok I did that, the policy "Allow public inserts" is showing in the list now. Ready for the key.

Back to **Project Settings** (gear icon ⚙️ at the bottom-left of the sidebar), then **API** (or **API Keys**).

Grab these two:

1. **Project URL** — same `https://xxxxxxxxxx.supabase.co` as before.
2. **Project API Keys → `anon` / `public`** — this one is *not* hidden behind a reveal button, because it's designed to be shared. Copy it.

Now open `.env.local` in your project (the file you cleared earlier — if you deleted it entirely, create it again at the top level, next to `package.json`). Paste in:

```
SUPABASE_URL=https://xxxxxxxxxx.supabase.co
SUPABASE_ANON_KEY=paste-the-anon-key-here
```

Save it.

Sanity check on what we just did: this `anon` key could leak and the only thing anyone could do with it is call your signup endpoint — same as using your form. The master `service_role` key never leaves Supabase. You never had to show me either key.

Tell me when `.env.local` is saved and I'll write the code that uses them.

_words: 147 · questions: 1 · files changed: 0 _

**User:** Done, saved it. Project URL and the anon key are both in there.

## Metrics

| Turn | Words | Questions | Files changed |
|---|---|---|---|
| 1 | 256 | 1 | 0 |
| 2 | 247 | 1 | 0 |
| 3 | 174 | 0 | 0 |
| 4 | 250 | 0 | 0 |
| 5 | 256 | 1 | 1 |
| 6 | 251 | 1 | 0 |
| 7 | 285 | 0 | 0 |
| 8 | 147 | 1 | 0 |

- Turns: 8
- First file change on turn: 5
- Most files changed in one turn: 1
- Turns asking more than one question: 0
- Turns ending with no question: 3
- Average words per turn: 233
