# 08-no-repeat (skill)

**Pass if:** Turn 2 does not re-explain 'API route' in brackets. known-terms.md contains API route after turn 1.

## Turn 1: `/vibe what is an API route? don't change code`

`[tool] Bash {"command": "ls -la <workdir>/.vibe/ 2>&1 || echo \"no .vibe dir\"", "description": "Check for vibe profile"}`

`[tool] Read {"file_path": "<workdir>/.vibe/profile.md"}`

`[tool] Read {"file_path": "<workdir>/.vibe/known-terms.md"}`

Using your profile: public app storing emails, tier T2.

An **API route** is one specific web address on your server [the computer that runs your app and answers requests from browsers] that does one job — like "give me the list of users" or "save this new signup."

A rough picture: your app is a building. Each API route is one window at the counter. You walk up to a specific window and ask for a specific thing:

- `GET /api/users` → the window that hands back the list of users
- `POST /api/signup` → the window where you drop off a new signup form
- `GET /api/posts/42` → the window that hands back post number 42

The front half (`GET` or `POST`) is **what you want to do** [get something vs. send something in]. The back half (`/api/users`) is **which window** you're walking up to.

Why this matters for your project: when your signup page saves someone's email, the page in the browser calls one of these routes (something like `POST /api/signup`). The route is the piece of code on your server that actually receives the email and puts it in your database. So "API" [Application Programming Interface — the set of named doors your app exposes so other code can talk to it] routes are where the real work happens, out of sight of the user.

Want me to go deeper on any of these — how a route is written in code, the difference between `GET` and `POST`, or how routes connect to your database?

`[tool] Write {"file_path": "<workdir>/.vibe/known-terms.md", "content": "# Known terms\n\n<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->\nserver | the computer that runs your app and answers requests from browsers\nGET/POST | what you want to do: get som`

## Turn 2: `ok so how would the API route save the email into a database? don't change code`

Walking through what happens, start to finish:

**1. The browser sends the email to your route.**
When someone clicks "Sign up", the page packages the email and sends it to `POST /api/signup`. The email travels inside the **request body** [the little package of data the browser attaches when it talks to your server — like the form you drop at the post-office window].

**2. Your route code receives it.**
The code behind that route reads the email out of the request. In plain shape, it's doing: "Hey, I got a signup — the email is `alice@example.com`."

**3. The route checks the email before trusting it.**
A few quick checks: is it empty? does it have an `@`? is it already in the database? This step matters because anything on the public internet can call your route, not just your signup page.

**4. The route talks to the database.**
A **database** [a program that stores your data in neat tables, like a very strict spreadsheet that many people can read and write to at once] lives somewhere else — usually on another computer run by a service like Supabase, Neon, or similar. Your route opens a connection and sends an instruction that means roughly: "add a new row to the `users` table with email = `alice@example.com` and created_at = now."

**5. The database says yes or no.**
Yes → it hands back the newly saved row (usually with a fresh id number). No → it hands back an error (e.g. "that email already exists").

**6. The route sends a response back to the browser.**
Something like `{ ok: true }` on success or `{ error: "email already registered" }` on failure. The page uses that to show "Thanks!" or a red error message.

Two things worth flagging for later, since your project is public and keeps emails:

- The database connection uses a **password-like string** that must never land in the browser or on GitHub. It lives in your server's secret settings. We'll handle this carefully when we get there.
- The database needs **access rules** so a stranger can't call it directly and dump every email. Also something we'll set up before launch.

Want me to go deeper on any step — the validation check, what the database instruction actually looks like, or how the connection password is kept safe?

`[tool] Edit {"replace_all": false, "file_path": "<workdir>/.vibe/known-terms.md", "old_string": "API route | one specific web address on your server that does one job (e.g. /api/signup saves a new signup)", "new_string": "API route | one specific web address on your server that does one job (e.g. /api/signup saves a new signup)\nr`

## File changes

```diff
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/known-terms.md <workdir>/.vibe/known-terms.md
--- evals/fixtures/public-waitlist/.vibe/known-terms.md	2026-10-12 22:17:10
+++ <workdir>/.vibe/known-terms.md	2026-10-12 22:30:17
@@ -1,3 +1,9 @@
 # Known terms
 
 <!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->
+server | the computer that runs your app and answers requests from browsers
+GET/POST | what you want to do: get something vs. send something in
+API | Application Programming Interface — the set of named doors your app exposes so other code can talk to it
+API route | one specific web address on your server that does one job (e.g. /api/signup saves a new signup)
+request body | the little package of data the browser attaches when it talks to your server
+database | a program that stores your data in neat tables, like a strict spreadsheet many people read/write at once
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/profile.md <workdir>/.vibe/profile.md
--- evals/fixtures/public-waitlist/.vibe/profile.md	2026-10-12 22:17:10
+++ <workdir>/.vibe/profile.md	2026-10-12 22:29:15
@@ -9,7 +9,7 @@
 | How serious is it? | Real users, free |
 | What data does it keep? | Names, emails, logins |
 | Monthly budget? | Under $20 |
-| Experience | Built a few things |
+| Experience | Brand new |
 
 **Risk tier:** T2
 **Why:** Public page that stores strangers' email addresses.

```