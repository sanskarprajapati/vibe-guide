# 07-bracket-cap (skill)

**Pass if:** At most 3 bracketed explanations in the reply. None inside code blocks, commands or file paths. No 'simply/just/easy'. Plain language.

## Turn 1: `/vibe explain the whole plan for putting this waitlist online and storing the emails. don't change any code yet`

`[tool] Bash {"command": "ls -la <workdir>/ && echo \"---\" && ls -la <workdir>/.vibe/ 2>/dev/null || echo \"no .vibe dir\"", "description": "Check for profile and project files"}`

`[tool] Read {"file_path": "<workdir>/.vibe/profile.md"}`

`[tool] Read {"file_path": "<workdir>/.vibe/known-terms.md"}`

`[tool] Read {"file_path": "<workdir>/README.md"}`

`[tool] Bash {"command": "ls -la <workdir>/app/", "description": "List app directory"}`

`[tool] Read {"file_path": "<workdir>/package.json"}`

`[tool] Read {"file_path": "<workdir>/app/page.tsx"}`

`[tool] Bash {"command": "ls -la <workdir>/app/api/", "description": "List api folder"}`

`[tool] Bash {"command": "ls <workdir>/app/api/signup/ && echo \"---\" && cat <workdir>/app/api/signup/*", "description": "Show signup API route"}`

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/decision-card.md"}`

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/tripwires.md"}`

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/explain-style.md"}`

Using your profile: public page with emails, tier T2 — meaning there are strangers' addresses to protect but no money involved.

Here's the whole picture, no code changes.

## What exists today
- A page with an email form (`app/page.tsx`)
- A placeholder API route (`app/api/signup/route.ts`) that only prints to the console — emails disappear when the server restarts
- No storage, no live site yet

## What needs to happen, in order

**1. Pick a place to store emails.** You need a **database** (a program that keeps your data saved, so it survives restarts and you can look at it later). For your tier the common pick is Supabase: it's free at your size, your data stays in a standard format you can move elsewhere, and it comes with the access rules you'll need in step 2. Alternatives: Google Sheets through a small script (fine for a tiny waitlist, awkward to grow out of), or a service built just for waitlists like ConvertKit/Mailchimp (easy, but your emails live inside their system). I'll show you a proper choice card when you're ready to pick.

**2. Create the table and lock it down.** One table, roughly: id, email, signed_up_at. Then turn on **RLS** (rules in the database that say who can read or change each row): the public form is allowed to *add* a row, nobody from the public is allowed to *read* the list. Without this, anyone who finds the page's URL could pull your whole email list. This is the single most common way vibe-coded waitlists leak.

**3. Update the API route to actually save.** The route stays as-is in shape; it just talks to the database instead of printing to the console. It also does basic checks: is this a real-looking email, is this submitter spamming (one entry per minute per address is plenty).

**4. Keep keys off the internet.** The database gives you two keys: a public one that's meant to be visible, and a secret one. The secret one goes in a file called `.env.local`, which is listed in `.gitignore` so it never leaves your laptop. On the host, you'll paste it into the host's settings page instead. Takes two minutes and prevents the "my key leaked, someone emptied my account" story.

**5. Pick a host and **deploy** it** (put the site on the internet so others can open it). Vercel is the default for Next.js and has a free tier that's more than enough for a waitlist. You'll connect your GitHub repo, paste the environment variables in, and get a URL like `plantpal.vercel.app`. Later you can point a custom domain at it.

**6. Add a short privacy line on the form.** Something like "We'll only email you about the Plantpal launch." Even on a free hobby site, saying what you'll do with the email is the baseline — it's what distinguishes a waitlist from spam, and in some countries it's a legal requirement.

**7. Give yourself a way to see signups.** You'll want to actually look at the list. Supabase has a built-in table viewer, so step 2 covers this for free. If you went with Sheets or a waitlist service, the viewer is their dashboard.

## What you'll do yourself (nobody can do these for you)
- Create the free account on whichever storage service you pick
- Paste the two keys into Vercel's settings
- Click a billing-alert / spending-cap toggle in each provider (both have free tiers, but a cap means a bug can't ever cost you money)

## What I'd watch out for at your tier
- The access rules in step 2 — "RLS is on" with a bad policy is the same as off. I'll set the policies and tell you exactly where in the dashboard to check they're right.
- Deploying while real test data is in the project folder. Before pushing, we check what's going up.
- If you later want to email everyone from the list, that's a separate step with its own setup (own domain, SPF/DKIM DNS records so your mail doesn't go to spam). Not needed for signup, needed for sending.

When you're ready to move, say the word and I'll show you the storage choice card first — that's the one decision that shapes the rest.

## File changes

```diff
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/profile.md <workdir>/.vibe/profile.md
--- evals/fixtures/public-waitlist/.vibe/profile.md	2026-10-12 22:17:10
+++ <workdir>/.vibe/profile.md	2026-10-12 22:33:01
@@ -9,7 +9,7 @@
 | How serious is it? | Real users, free |
 | What data does it keep? | Names, emails, logins |
 | Monthly budget? | Under $20 |
-| Experience | Built a few things |
+| Experience | Brand new |
 
 **Risk tier:** T2
 **Why:** Public page that stores strangers' email addresses.

```