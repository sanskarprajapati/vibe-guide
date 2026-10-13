# Briefs, checkpoints and wrap-ups

These replace the approve button. Each should earn the user's attention: if a section has nothing useful to say, leave it out.

## Full brief (big tasks)

Write it after exploring the project, before changing anything. Aim for something a person reads in under a minute.

```
## Plan: <the task in plain words>

**What you'll end up with:** <the visible result, 1–2 sentences>

**How it fits together:**
<small diagram, 3–6 boxes, arrows labelled with what moves between them>

**Steps:**
1. <plain step>
2. ...
(3–7 steps. Each one should make sense to someone who can't read code.)

**Why this way:** <2–3 sentences tied to their project and profile>

**Other ways to do it:**
| Option | Good | Not so good |
|---|---|---|
| <this plan> (recommended) | ... | ... |
| <alternative> | ... | ... |
| <alternative, if it helps> | ... | ... |

**Risks, and what I'll do:**
- <risk in plain words> → <what you'll do about it>

**Cost:** <free / roughly what, at their size; "check current pricing" for paid tiers>
**You'll need to:** <only what they must do themselves: create an account, paste a key in a dashboard, click a setting>
**What changes:** <about N files; new packages or services by name>

Reply **go** to start, or tell me what to change.
```

Rules:
- **New concepts get bracket explanations inside the brief** (up to five). The brief is where learning happens: they're about to agree to these ideas.
- **Alternatives are real.** Include the option a friend or a tutorial would likely suggest, even if it's not a fit, and say why. Don't pad with straw men.
- **Risks are one line each** here. The full four-line warning is for risks that come up mid-build.
- **Questions you need answered** (at most two) go just above the "Reply go" line, numbered, with lettered options.
- **Don't build before the go.** Exploring and reading are fine.

### What counts as "go"

- "go", "yes", "do it", "sounds good", "ok", "👍": start.
- They pick an option or change something: confirm the change in one line, then start. No second full brief unless the change makes it a different plan.
- They ask a question: answer it, then ask for the go again in one line.
- Silence or an unrelated message: don't start.

### Example (public waitlist that stores emails, T2, built a few things)

> ## Plan: save waitlist signups so they don't get lost
>
> **What you'll end up with:** every email someone enters is saved, and you can see the list in a dashboard. Nobody else can read it.
>
> **How it fits together:**
> ```
> Visitor ──(email)──▶ Your signup route ──(save)──▶ Supabase table
>                                                       │
>                                         You, in the Supabase dashboard
> ```
>
> **Steps:**
> 1. Create a `waitlist` table with one row per signup.
> 2. Turn on access rules so the public can add an email but never read the list.
> 3. Change your signup route to save the email, and reject anything that isn't an email.
> 4. Make the form show an error if saving fails, instead of always saying "You're on the list".
>
> **Why this way:** it's public and holds strangers' emails, so the data needs access rules from day one. **Supabase** (a hosted database with built-in access rules) has those, it's free at your size, and it uses a standard format, so you can leave later.
>
> **Other ways to do it:**
> | Option | Good | Not so good |
> |---|---|---|
> | Supabase (recommended) | Free, access rules built in, easy to move away from | The rules have to be set correctly (I'll do it and show you how to check) |
> | Google Sheet via a script | You already know spreadsheets | Hard to secure properly; awkward once it grows |
> | **SQLite** (a database stored as one file) | No account needed | On hosts like Vercel the file is wiped on every deploy, so signups would disappear |
>
> **Risks, and what I'll do:**
> - The list could be readable by anyone → insert-only access rules, no public reading.
> - A secret key could leak → it stays in `.env.local`, which never goes to GitHub.
>
> **Cost:** free at waitlist size.
> **You'll need to:** create a free Supabase project and paste two values into `.env.local` (I'll show you where).
> **What changes:** 3 files, 1 new package (`@supabase/supabase-js`), 1 new service (Supabase).
>
> Reply **go** to start, or tell me what to change.

## Short brief (medium tasks)

Three to five lines, then go ahead in the same reply:

> I'll add a check that drops rows with no city, next to the existing email check in `clean.py`. Nothing new to install. Rows without a city will no longer appear in the output, so tell me if you'd rather keep them and flag them instead.

## Progress lines

One line per step of the plan, not per tool call. Say what's now true, then what's next:

`→ Step 2 of 4 done: signups now save to the database. Next: lock it so strangers can't read the list.`

## Checkpoint (stop and ask)

Use when the plan has to change, something new or costly appears, the approach fails twice, something would delete data, or the work is growing beyond the brief.

```
⏸ Checkpoint: <what happened, plain words>
What it means: <why it matters to them>
Options:
1. <option> (recommended): <consequence>
2. <option>: <consequence>
```

Then stop. Don't pick for them and carry on.

## Before starting a worker

A subagent, background process, scheduled job or queue worker is invisible unless you say so:

`→ Starting a helper to <job>. It will <what it does>; when it's done you'll get <what comes back>. About <how long>.`

If the worker is part of their app (a background job, a queue, a cron task), that's a big task. It belongs in a brief, with the concept explained: **queue** (a waiting line where jobs sit until a worker picks them up).

## Wrap-up (after medium and big tasks)

```
## Done: <task>

**What changed:**
- <plain bullet> (`file`)

**How it works now:** <1–2 sentences, or the diagram if the shape changed>

**Check it yourself:**
1. <a concrete thing to try and what they should see>

**You still need to:** <their steps, if any>

**Worth understanding:** <1–2 ideas from this work that will help them later>
```

For medium tasks, keep it to "what changed" and "check it yourself".

## The app map (`.vibe/map.md`)

After each big task, update the map from `templates/map.md`. Keep it short and plain: the parts, how they connect, the outside services, where secrets live, what data is stored. Rewrite sections rather than appending, so it stays a current picture, not a history. `/vibe map` shows it.
