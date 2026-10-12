# 07-bracket-cap (skill)

**Pass if:** At most 3 bracketed explanations in the reply. None inside code blocks, commands or file paths. No 'simply/just/easy'. Plain language.

## Turn 1: `/vibe explain the whole plan for putting this waitlist online and storing the emails. don't change any code yet`

`[tool] Bash {"command": "ls -la <workdir>/ && ls -la <workdir>/.vibe/ 2>/dev/null || echo \"no .vibe dir\"", "description": "Check for profile and project files"}`

`[tool] Read {"file_path": "<workdir>/.vibe/profile.md"}`

`[tool] Read {"file_path": "<workdir>/.vibe/known-terms.md"}`

`[tool] Bash {"command": "ls <workdir>/app/ && cat <workdir>/package.json <workdir>/README.md", "description": "Peek at the app to understand what exists"}`

`[tool] Read {"file_path": "<workdir>/app/page.tsx"}`

`[tool] Bash {"command": "ls <workdir>/app/api/ && find <workdir>/app/api -type f", "description": "Look at the API route"}`

`[tool] Read {"file_path": "<workdir>/app/api/signup/route.ts"}`

Using your profile: public page storing strangers' emails, tier T2, brand new to coding, budget under $20/mo.

Here's the whole plan in plain words. Nothing to decide yet — just the shape of it.

### What you have today
A Next.js page with a form that posts to `/api/signup`, which currently just prints the email to the terminal and throws it away. Nothing is saved. Nothing is online.

### What has to be true for real users

1. **The page has to live somewhere public.** Right now it only runs on your laptop. It needs to go on a host [hosting = a company that runs your site on their computers so anyone on the internet can open it in a browser]. For Next.js, Vercel is the natural fit and has a free tier that covers a waitlist.

2. **Emails need to go somewhere that survives.** `console.log` prints and vanishes. You need a database [database = organized storage that keeps data between restarts, so you can look at the list a week later]. For your tier and budget the realistic beginner options are Supabase, Resend's "audiences" feature (built exactly for waitlists), or an Airtable base. They trade off differently — I'll lay those out side by side when you're ready to pick.

3. **The API route needs a secret to reach the database.** That secret lives in an environment variable [environment variable = a value the host hands to your code at runtime, so the secret isn't typed into your source code and accidentally pushed to GitHub]. You paste it into the host's dashboard once; nobody else sees it.

4. **The database needs access rules.** Because the page is public, anyone on the internet can hit `/api/signup`. You want *writes* to succeed, but you do **not** want strangers to be able to read the whole email list through the database. This step is easy to forget and is the single most common way waitlists leak.

5. **The form needs a few sanity checks before launch.** Today it accepts anything. You'll want: real email-format check on the server, basic bot/spam protection, and a per-IP rate limit so one script can't submit 10,000 fake emails overnight.

6. **A one-line privacy note under the form.** You're collecting personal data from strangers, so something like "we'll email you once about Plantpal, nothing else" covers the basics for most places.

### The order I'd do it in
1. Pick the database (biggest decision — shapes the next three steps)
2. Wire `/api/signup` to that database
3. Put the project on GitHub
4. Deploy to the host and paste the database secret into its dashboard
5. Turn on the database access rules + add email validation, spam check, rate limit, privacy line
6. Test the live form yourself, then share the link

### Not in the plan
- No login system — you're gathering emails, not creating accounts
- No payments
- No actual email-sending yet — the launch email comes later; for now you're just collecting addresses

### What comes up first when you're ready
The database choice. The three options above differ in: how much code you write vs. how much you click in a dashboard, whether you can view the list in a spreadsheet, and whether sending the launch email later is one more click or a separate setup.

Want me to walk through the database choice next, or dig into any step above?

`[tool] Write {"file_path": "<workdir>/.vibe/known-terms.md", "content": "# Known terms\n\n<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->\nhosting | a company that runs your site on their computers so anyone on the internet can open it in a browser\ndat`

## File changes

```diff
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/known-terms.md <workdir>/.vibe/known-terms.md
--- evals/fixtures/public-waitlist/.vibe/known-terms.md	2026-10-12 22:17:10
+++ <workdir>/.vibe/known-terms.md	2026-10-12 22:30:10
@@ -1,3 +1,6 @@
 # Known terms
 
 <!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->
+hosting | a company that runs your site on their computers so anyone on the internet can open it in a browser
+database | organized storage that keeps data between restarts, so you can look at the list a week later
+environment variable | a value the host hands to your code at runtime, so the secret isn't typed into your source code and accidentally pushed to GitHub
diff -ruN -x .claude evals/fixtures/public-waitlist/.vibe/profile.md <workdir>/.vibe/profile.md
--- evals/fixtures/public-waitlist/.vibe/profile.md	2026-10-12 22:17:10
+++ <workdir>/.vibe/profile.md	2026-10-12 22:28:51
@@ -9,7 +9,7 @@
 | How serious is it? | Real users, free |
 | What data does it keep? | Names, emails, logins |
 | Monthly budget? | Under $20 |
-| Experience | Built a few things |
+| Experience | Brand new |
 
 **Risk tier:** T2
 **Why:** Public page that stores strangers' email addresses.

```