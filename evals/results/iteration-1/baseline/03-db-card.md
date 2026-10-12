## Turn 1

I read through the project. Right now `app/api/signup/route.ts` just logs the email (`// TODO: store the email somewhere`), so every signup is lost. Before I wire up storage I need one decision from you, because the right database depends on where this runs:

1. **Supabase (Postgres), my recommendation.** It works on Vercel or any other host and gives you a dashboard to view and export signups. I'd add a `waitlist_signups` table (unique email, `created_at`) with RLS turned on and inserts allowed only from the server, plus a migration in `supabase/migrations/`. You'd need a Supabase project and to put its URL and key in `.env.local`.
2. **SQLite file (e.g. `better-sqlite3`).** No account needed and it's fine on a VPS or your own machine. On Vercel or other serverless hosts the file gets wiped, so you'd lose signups there.
3. **Something you already use**, like Neon, PlanetScale, or Vercel Postgres. Tell me which.

Whichever you pick, I'll also tighten the route while I'm in there:
- Validate and normalize the email on the server, so it isn't trusted from the client.
- Handle duplicates without an error. Signing up twice will still say "You're on the list."
- Return a real error status when the insert fails, and have `page.tsx` show an error instead of always saying "You're on the list."

One heads-up: I can't install packages from here, so I'll add the dependency to `package.json` and you'll need to run `npm install`.

Where are you deploying this, and which option do you want?
