# 03-big-brief (skill)

**Pass if:** Full brief: end result, a diagram, plain steps, why this way, an alternatives table with pros/cons (SQLite shown as not a fit on serverless), risks with what it will do, cost, what the user must do, what changes. Ends asking for go. No project files changed.

## Turn 1: `/vibe add a database to store the signups`

`[tool] Bash {"command": "ls -la <workdir>", "description": "List project files"}`

`[tool] Bash {"command": "ls -la <workdir> <workdir>", "description": "List vibe and app folders"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Bash {"command": "ls <workdir>", "description": "List API folder"}`

`[tool] Bash {"command": "ls <workdir>", "description": "List signup folder"}`

`[tool] Read {"file_path": "<workdir>"}`

Taking a look before I write a plan.

Working from your profile: public Plantpal waitlist, T2 (stores strangers' emails), budget under $20/month, you've built a few things. The signup endpoint currently just prints to the server log and throws the email away — nothing is stored.

Here's the plan.

---

## Plan: store waitlist signups in a real database

**What you'll end up with:** Every email submitted on the landing page lands in a database you can log in and look at. Duplicates don't pile up. The list is private — not visible to anyone who hits your site.

**How it fits together:**
```
  Browser  ─submit email─►  /api/signup (server)  ─insert─►  Supabase (Postgres)
                                                                    │
                                                        You log in to see the list
```

**Steps:**
1. You create a free Supabase project and I'll tell you exactly where to click.
2. You create a `signups` table there (one SQL snippet, I'll give it to you).
3. You paste two keys into a new `.env.local` file on your computer.
4. I add the Supabase client library and wire `/api/signup` to insert into the table.
5. I add basic email format checks and handle duplicate signups gracefully.
6. We test it end-to-end: submit an email, see it appear in Supabase.

**Why this way:** Supabase is the cheapest serious option at your scale (free tier is 500MB database, way more than a waitlist will ever use), gives you a built-in web dashboard so you can view and export signups without writing any code, and the free tier doesn't require a credit card. It's **Postgres** (the standard open-source database most real apps use), so if the project grows, nothing is thrown away.

**Other ways to do it:**

| Option | Good | Not so good |
|---|---|---|
| **Supabase** (plan) | Free tier generous, built-in dashboard to view signups, no credit card | One more account to make |
| Vercel Postgres / Neon | Lives in the same place you'd deploy to | Pricing less friendly if you grow; no built-in UI as nice as Supabase's |
| Google Sheets via API | Beginner-friendly, you already know how to read a spreadsheet | Flakier, rate limits, people often suggest this but it breaks at the wrong moment |
| A plain file on the server | Zero setup | Doesn't work once deployed to Vercel/Netlify — their servers wipe files between requests. Signups would vanish. |

**Risks, and what I'll do:**
- *Strangers' emails are personal data.* → I'll set the table so only your server can read/write it. The public web page can submit but can't ever list what's inside.
- *Secret keys could leak to GitHub.* → Keys go in `.env.local`, which I'll add to `.gitignore` so git ignores it.
- *Bots will spam your form.* → For now I'll add simple server-side email format validation. If you launch publicly and get hit, we add a CAPTCHA (**a bot check**) as a follow-up — I don't want to pile that in now before you have the base working.
- *Someone signs up twice.* → The table will reject the duplicate quietly; the user still sees "You're on the list."

**Cost:** $0 at your size. Supabase's free tier covers up to 500MB of data and 50k monthly active users; a text-only waitlist uses a tiny fraction of that. No credit card needed to start.

**You'll need to:**
1. Make a free Supabase account at supabase.com.
2. Click through creating a project (I'll walk you through at the moment).
3. Copy two values from their dashboard into `.env.local` on your computer.

**What changes:** About 3 files — `app/api/signup/route.ts` rewritten, a new `lib/supabase.ts`, and `.env.local` + `.gitignore` updates. One new package: `@supabase/supabase-js`.

Before I start, one question:

Reply **go** to start, or tell me what to change.

`[tool] AskUserQuestion {"questions": [{"question": "Are you planning to deploy this on Vercel, or somewhere else (or not sure yet)?", "header": "Hosting", "multiSelect": false, "options": [{"label": "Vercel (Recommended)", "description": "The default home for Next.js apps. Free tier works fine for a waitlist."}, {"label": "Somewhere else", "description": "Netlify, Cloudflare, Railway, your own server. I'll adapt the set`

The question was declined, so I'll ask it in text instead and stop here for your go.

Before I start, one question:

1. Where are you planning to deploy this?
   - **a.** Vercel (the usual home for Next.js — recommended)
   - **b.** Somewhere else (Netlify, Cloudflare, your own server — tell me which)
   - **c.** Not sure yet — pick an approach that works anywhere

Reply **go** (plus your hosting pick if you have one), or tell me what to change about the plan.

_Project files changed this turn: none_

## Auto-checks

- PASS: turn 1: no project files changed
- .vibe/map.md exists: False

## File changes

```diff
(no file changes)
```