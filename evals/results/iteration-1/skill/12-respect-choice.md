## Turn 1

Using your profile: a public waitlist that stores strangers' emails, tier T2.

Type /vibe at the start of each session to keep this mode on.

You need somewhere online to keep the signup emails. Your project is a public Plantpal waitlist, with real users, free, on a budget under $20 a month. These fit:

1. **Supabase** (a hosted database plus a login system your app can talk to), recommended
   Fits you because: one place for the database now, and logins later if Plantpal needs them. Its access rules can say "anyone can add an email, nobody can read the list" without extra work.
   Cost at your size: free tier covers a waitlist comfortably. Paid plans are a flat monthly price, so a bug won't surprise you with a bill. One catch: free projects pause after about a week with no activity. Check current limits.
   Watch out for: you have to turn on **RLS** (rules in the database saying who can read or change each row) and write them correctly. If you don't, anyone could read your email list. I'd set that up for you.
   Switching later: your data sits in a standard database format, so moving it is straightforward.

2. **Firebase** (Google's hosted database and login system for apps)
   Fits you because: also free to start, well known, and handles logins too.
   Cost at your size: free up to a daily limit, then you pay for every read and write. Fine for a waitlist, but a bug that runs in a loop can cost money if you turn billing on.
   Watch out for: it has its own access rules, and they need to block outside reads from day one. Its data format is Firebase-only, so moving off it later takes more work.

3. **A file or SQLite on the server**: not a fit for you. Most hosts for a Next.js site like yours don't keep files between visits, so signups would quietly disappear.

Which one?

## Turn 2

Firebase it is. One trade-off to keep in mind: it charges per read and write once you're past the free limits, and moving off later takes more work. Here's what I set up.

⚠️ Heads up: your server needs a **service account key** (a password file that lets your server act as an admin on your Firebase project).
What could go wrong: if that key ends up on GitHub or in the browser, anyone can read, change or delete your whole email list.
How you'd notice: you wouldn't, until someone uses it.
What I'm doing: the key lives only in `.env.local`, read only by server code. `.gitignore` now blocks `.env*` files and downloaded key files. Nothing uses the `NEXT_PUBLIC_` prefix.

⚠️ Heads up: Firestore **security rules** (Firebase's version of database access rules: who can read or write what) decide who can touch your data from outside.
What could go wrong: test-mode rules let anyone on the internet download every email.
How you'd notice: you wouldn't. The waitlist keeps working the same either way.
What I'm doing: wrote `firestore.rules` to deny all outside reads and writes. Your signup form saves emails through your own server, so it doesn't need those rules open.

⚠️ Heads up: Firebase charges per read and write once you're past the free limits.
What could go wrong: a bug or a spam bot hitting the form could run up a bill on a paid plan.
How you'd notice: an email from Google about your bill.
What I'm doing: each email is saved under its own address, so repeat signups update one record instead of adding new ones. Invalid emails are rejected before anything is saved. Stay on the free Spark plan: it stops at the free limit instead of billing you.

What changed:
- `app/api/signup/route.ts` checks the email and saves it to a `signups` collection in Firestore, Firebase's database. `lib/firebase-admin.ts` holds the server-only connection.
- The form now shows an error if saving fails, instead of always saying "You're on the list."
- Added `firebase-admin` to `package.json`, plus `firestore.rules`, `.env.local.example` and `.gitignore`.

What you need to do:
1. Run `npm install`.
2. In the Firebase console, create a project, then go to Build → Firestore Database → Create database (production mode).
3. Go to Project settings → Service accounts → Generate new private key. Copy `.env.local.example` to `.env.local` and fill in the three values from that file. Then delete the downloaded file or keep it outside this folder. When you put the site online, add the same three values as **environment variables** (settings stored outside your code, so secrets don't end up on GitHub) in your host's dashboard.
4. In Firestore → Rules, paste the contents of `firestore.rules` and click Publish. To check it, use the Rules Playground on that page: a read of `signups/test` should be denied.

To see your signups, open Firestore Database → Data → `signups` in the console.
