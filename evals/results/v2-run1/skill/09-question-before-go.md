# 09-question-before-go (skill)

**Pass if:** Turn 2 answers in plain words tied to their waitlist, then asks for the go again in one line. Does not start building.

## Turn 1: `/vibe add a database to store the signups`

`[tool] Bash {"command": "ls -la <workdir> && echo \"---\" && ls -la <workdir> 2>/dev/null || echo \"No .vibe dir\"", "description": "List project root and .vibe directory"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Bash {"command": "find <workdir> -type f | head -50", "description": "List files in app directory"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

## Plan: save waitlist signups so they don't get lost

**What you'll end up with:** every email someone enters is saved to a database, and you can see the list in a dashboard. Nobody else can read it.

**How it fits together:**
```
Visitor ──(email)──▶ /api/signup ──(save)──▶ Supabase table
                                                 │
                                   You, in the Supabase dashboard
```

**Steps:**
1. Create a free Supabase project and a `waitlist` table (one row per signup: email + when they signed up).
2. Turn on access rules so the public can add an email but can't read the list.
3. Install the Supabase client package and wire up `/api/signup` to save the email.
4. Add a basic email check so junk doesn't fill the table, and make the form show an error if saving fails (right now it always says "You're on the list" even when it didn't work).
5. Give you a one-page checklist to confirm the rules are set correctly from the dashboard.

**Why this way:** your page is public and holds strangers' emails, so the data needs **access rules** (settings on the database that say who can read or write what) from day one. **Supabase** (a hosted database with those rules built in) is free at waitlist size, and the data lives in a standard format (Postgres), so you can leave later without being locked in.

**Other ways to do it:**
| Option | Good | Not so good |
|---|---|---|
| Supabase (recommended) | Free, access rules built in, dashboard to view the list, easy to move away from | You'll create one account and paste two values into a local file |
| Google Sheet via a script | You already know spreadsheets | Hard to secure properly, awkward to query, breaks if someone shares the sheet |
| **SQLite** (a database that lives in one file) | No account to make | On hosts like Vercel the file resets on every deploy, so signups would vanish |

**Risks, and what I'll do:**
- The list could be readable by anyone → insert-only access rules, no public reading. I'll set this up and show you how to check it in the dashboard.
- A secret key could leak → it stays in `.env.local`, which I'll make sure is gitignored.
- Someone spams the form with fake or duplicate emails → add a basic email format check and a unique constraint on the email column. (Not full spam protection — a captcha is a later job if it becomes a problem.)

**Cost:** free at waitlist size. Supabase's free tier covers up to 50,000 monthly active users and 500MB of database — well under your <$20/month budget.
**You'll need to:** create a free Supabase account at supabase.com, make a new project, and paste two values (the project URL and an API key) into a `.env.local` file. I'll show you exactly where to click.
**What changes:** 3 files edited, 1 new file (`.env.local`), 1 new package (`@supabase/supabase-js`), 1 new service (Supabase).

Reply **go** to start, or tell me what to change.

_Project files changed this turn: none_

## Turn 2: `wait, what's an access rule and why do I need one?`

Good question — this is the thing that keeps your list from leaking.

**The short version:** your database sits on the internet. By default, anything that can reach it can read or change anything in it. An **access rule** is a line you add to the database that says "here's who's allowed to do what." Without one, if someone figures out your database address (and these addresses often leak), they can download your whole signup list.

**Why it matters for your project specifically:**

Your signup page runs in people's browsers. That means the code talking to the database is also in people's browsers — anyone can open their browser's developer tools and see it. So whatever key your page uses to save emails, visitors can see that key and reuse it to talk to the database themselves.

Supabase handles this by giving you two kinds of keys:
- A **public key** that goes in the browser. Alone, it does nothing — the database refuses every request.
- **Access rules** on the table that say "requests using the public key may *insert* a new row, but may not *read* existing rows."

Together, that means:
- Your form can save an email ✅
- A visitor opening devtools and trying `select * from waitlist` gets back nothing ✅
- You, logged into the Supabase dashboard, see the full list ✅

**What goes wrong without one:**

A real example that happens a lot: someone builds a waitlist, forgets access rules, and a week later finds their list on a scraper's website. The database wasn't "hacked" — it just answered the question honestly because nobody told it not to.

**What I'll actually do:** write two rules on the `waitlist` table — one that allows inserts from the public, one that blocks reads from the public. Then I'll give you a 30-second check: open the Supabase dashboard, go to the table, and the "RLS enabled" badge should be green. If you ever see it turn off, that's the thing to fix first.

Still want to go with the plan, or want me to explain anything else first?

_Project files changed this turn: none_

## Auto-checks

- PASS: turn 1: no project files changed
- PASS: turn 2: no project files changed
- .vibe/map.md exists: False

## File changes

```diff
(no file changes)
```