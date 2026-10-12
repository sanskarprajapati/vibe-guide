## Turn 1

Using your profile: public page that stores strangers' emails, tier T2.
Type /vibe at the start of each session to keep this mode on.

Supabase has two keys, and only one of them can go in the frontend.

⚠️ Heads up: a Supabase key is going into code that every visitor's browser downloads.
What could go wrong: the **service_role key** (Supabase's master key that ignores every access rule) in the frontend lets anyone read, change or delete your whole waitlist. Bots scan websites for it within minutes.
How you'd notice: you wouldn't. The form works the same either way, until someone dumps your email list.
What I'm doing: the frontend only uses the **anon key** (Supabase's public key, meant to be seen, safe only with access rules on). The service_role key isn't used anywhere.

⚠️ Heads up: I'm creating the table that holds the emails and deciding who can touch it.
What could go wrong: since the anon key is public, anyone can copy it out of your site. Without access rules, or with a rule that allows everyone, they could download every email on the list.
How you'd notice: you wouldn't. Nothing looks broken.
What I'm doing: turning on **RLS** (rules inside the database saying who can read or add each row) with one rule: visitors can add an email, and that's all. No reading, editing or deleting with the public key.

What I changed:
- `app/page.tsx`: the form now saves the email straight to Supabase. If the email is already on the list, the visitor still sees "You're on the list." If something fails, they get a short error message.
- `lib/supabase/client.ts`: connects to Supabase using the URL and anon key from your settings, not hard-coded values.
- `supabase/migrations/20261012000000_create_waitlist.sql`: creates the `waitlist` table (no duplicate emails, basic email format check), turns on RLS and adds the add-only rule.
- `.env.example` shows which settings to fill in. `.gitignore` keeps your real `.env.local` off GitHub.
- `package.json`: added the two official Supabase libraries.

What you need to do:
1. Run `npm install`.
2. Copy `.env.example` to `.env.local`. In Supabase, open Project Settings → API (it may be called "API Keys"), then paste the Project URL and the **anon / publishable** key. Leave the key labelled `service_role` or "secret" where it is.
3. In Supabase, open SQL Editor, paste in the contents of the migration file and click Run.
4. To check it yourself: Authentication → Policies should list one insert policy on `waitlist` and nothing else. The Security Advisor shouldn't flag the table.

One more thing: `app/api/signup/route.ts` isn't used anymore. Want me to remove it? The other option is to save emails through that server route instead of from the browser. That way we could later limit how many signups one visitor can send, which the browser-only version can't do.
