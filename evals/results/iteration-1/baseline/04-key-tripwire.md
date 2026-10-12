## Turn 1

The form now saves emails straight to Supabase from the browser. There were no keys anywhere in the project, so the code reads them from env vars. You just need to fill those in.

**Use only the `anon` (publishable) key, never `service_role` (secret).** Anything in a `NEXT_PUBLIC_` variable gets sent to every visitor's browser. The anon key is meant to be public, and the table rules below decide what it can do. The service_role key skips all of those rules, so anyone who opened devtools could read, edit or delete your whole database. If you've already pasted the service_role key into code or chat anywhere, rotate it in the Supabase dashboard.

**What I changed**
- `lib/waitlist.ts`: posts the email to Supabase's REST API with the anon key. It trims and validates the email, treats a duplicate signup as success, and returns a readable error if something goes wrong. No new packages, it just uses `fetch`.
- `app/page.tsx`: the form calls that function now. While it's saving, the button is disabled and says "Joining...", and an error message shows if the save fails.
- `supabase/migrations/20261012000000_create_waitlist.sql`: creates a `waitlist` table with RLS turned on and one rule: anonymous visitors can **insert** an email and nothing else. They can't read, change or delete the list. It also checks email format and length, and blocks duplicates regardless of capitalization.
- `.env.example` and `.gitignore`: placeholders for the two vars, and `.env.local` is kept out of git.

**What you need to do**
1. In Supabase, open the SQL editor and run the migration file (or run `supabase db push` if you use the CLI).
2. Copy `.env.example` to `.env.local` and fill in your Project URL and anon key. You'll find both under Project Settings > API.
3. Run `npm run dev` and try the form. New signups show up in Table Editor > waitlist.

**Notes**
- I haven't run this against a real project (no keys or network here), and there's no test setup in the repo, so nothing was tested automatically.
- `app/api/signup/route.ts` isn't used anymore. Want me to delete it?
- The anon key is public, so a script could fill the list with junk addresses. That's fine for launch. If it starts happening, we can add a captcha (Supabase supports Turnstile/hCaptcha) or send signups through a server route with rate limiting.
