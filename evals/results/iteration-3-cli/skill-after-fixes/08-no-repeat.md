# 08-no-repeat (skill)

**Pass if:** Turn 2 does not re-explain 'API route' in brackets. known-terms.md contains API route after turn 1.

## Turn 1: `/vibe what is an API route? don't change code`

`[tool] Bash {"command": "ls -la <workdir>/.vibe/ 2>/dev/null && echo \"---\" && cat <workdir>/.vibe/profile.md 2>/dev/null && echo \"---TERMS---\" && cat <workdir>/.vibe/kn`

Using your profile: public page with emails, tier T2.

**What's an API route?**

Think of your app in two halves. The **frontend** (the part people see in their browser) and the **backend** (the code that runs on a server somewhere else, that the browser can't see). An API route is a specific door into the backend.

Each route has:
- A **URL path** — like `/api/signup` or `/api/send-email`
- A piece of code behind it that runs when someone knocks on that door
- Something it sends back (usually data, like "ok, user created" or "here's your list of posts")

A simple way to picture it: a company phone system. Dial 101, you get sales. Dial 102, you get support. Same idea — each URL path triggers a different job.

**A tiny example of what one does:**
- Someone types their email on your signup page.
- The browser sends that email to `/api/signup`.
- The code at that route saves the email to your database and emails them back.
- The browser gets a reply like "done" and shows a success message.

**Why they matter for you:** anything that touches secrets, your database, or paid services (like sending email) usually lives behind an API route — not in the browser code — so that visitors can't see or mess with it. For a T2 project storing emails and logins, almost all the sensitive work will happen in routes like these.

Want me to go deeper on any part — how a route gets built, or how it keeps your database password hidden from users?

`[tool] Write {"file_path": "<workdir>/.vibe/known-terms.md", "content": "# Known terms\n\n<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->\nAPI route | a specific URL on your backend that runs a piece of code when the browser (or something else) knocks on `

`[tool] Read {"file_path": "<workdir>/.vibe/known-terms.md"}`

`[tool] Write {"file_path": "<workdir>/.vibe/known-terms.md", "content": "# Known terms\n\n<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->\nAPI route | a specific URL on your backend that runs a piece of code when the browser (or something else) knocks on `

Saved those three terms (API route, frontend, backend) so I won't re-explain them next time. No code was changed.

## Turn 2: `ok so how would the API route save the email into a database? don't change code`

Here's the flow, step by step. Say the route is `/api/signup`:

1. The browser sends `{ email: "alex@example.com" }` to that URL.
2. The route's code reads that email out of the request.
3. The code calls a **database** (an organized storage system — think a spreadsheet with superpowers) through a **library** (prewritten code someone made that you plug into yours, so you don't build everything from scratch) and asks it to save a new row.
4. The database writes it to a table like `users` and sends back a confirmation.
5. The route sends `{ ok: true }` back to the browser, which can now show "thanks, you're signed up."

The code at step 3 is basically telling the database: "insert into the `users` table a new row where email = 'alex@example.com'."

Two things that already matter at your tier (T2, public, storing emails) — just so they're on your radar when we get there:

- **The database password never lives in frontend code.** It lives in an **environment variable** (a secret setting stored outside your code, so passwords don't end up in files you might share). Only the backend route can read it.
- **Who's allowed to write and read.** Databases usually accept anything from whoever has the password. For a public app, you'd set up rules so that only your signup route can add users, and random visitors can't read other people's emails. We'll turn those on when you pick a database — I'll set it up, not quiz you on it.

Want to go deeper on which part — what the actual insert command looks like, or how the route stops someone from spamming it with fake signups?

`[tool] Write {"file_path": "<workdir>/.vibe/known-terms.md", "content": "# Known terms\n\n<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->\nAPI route | a specific URL on your backend that runs a piece of code when the browser (or something else) knocks on `

Logged database, library, and environment variable so I won't re-explain them. No code changed.

## File changes

```diff
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/known-terms.md <workdir>/.vibe/known-terms.md
--- evals/fixtures/public-waitlist/.vibe/known-terms.md	2026-10-12 22:17:10
+++ <workdir>/.vibe/known-terms.md	2026-10-12 22:34:16
@@ -1,3 +1,9 @@
 # Known terms
 
 <!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->
+API route | a specific URL on your backend that runs a piece of code when the browser (or something else) knocks on it
+frontend | the part of your app people see in their browser
+backend | code that runs on a server somewhere else, that the browser can't see
+database | an organized storage system — think a spreadsheet with superpowers
+library | prewritten code someone made that you plug into yours, so you don't build everything from scratch
+environment variable | a secret setting stored outside your code, so passwords don't end up in files you might share
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