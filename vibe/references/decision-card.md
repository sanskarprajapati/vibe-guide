# Comparing options

The most common way beginners get hurt is the AI quietly picking a popular default that doesn't fit: a cloud database for a laptop script, pay-per-use hosting on a $0 budget, three separate services where one would do. Comparing options makes the choice visible and lets them make it.

**Inside a full brief**, the comparison is the "Other ways to do it" table (see `briefing.md`). Use the rules and starting points below to fill it in.

**On its own**, use the card template below when they ask "what should I use for X?" without asking you to build anything yet.

## When a comparison is needed

Compare options before adding any of these:
- database or file storage
- login / auth provider
- hosting or deploy platform
- email sending, payments, analytics, search, AI/LLM API
- any service with an account, an API key or a bill

Also show one when they ask "what should I use for X?"

**Skip the card** for small standard libraries (a date formatter, a validation library, an icon set). Add them and mention them in one line. Skip it at T0 when the obvious answer is local (a file or SQLite) and nothing hosted is involved. Say what you chose and why in one sentence.

## Template

Re-read `.vibe/profile.md` first.

```
You need <capability in plain words>. For <one-line profile summary>, here's what fits:

1. **<Option>** (<plain explanation>), recommended
   Fits you because: <tie to their profile>
   Cost at your size: <shape of pricing at their scale>
   Watch out for: <the main catch>

2. **<Option>** (<plain explanation>)
   Fits you because: ...
   Cost at your size: ...
   Watch out for: ...

3. **<Option>**: not a fit for you, because <reason tied to profile>
```

Then ask with `AskUserQuestion`: recommended option first, labelled "(Recommended)". If `AskUserQuestion` isn't available, end with "Which one?" and stop. Don't write integration code before they answer.

## Rules

- **2–3 options.** A "not a fit" option is useful when it's the one they'd hear about elsewhere.
- **Cost at their scale, not list prices.** Say the shape: "free until about 50,000 monthly users, then paid", "charges per database read, so a bug in a loop can cost money". Don't state exact dollar figures from memory; prices change. If a number matters, say "check current pricing" or look it up.
- **Name the lock-in.** How hard is it to switch later? "Your data is plain Postgres, so you can move it" vs "rules and data format are Firebase-specific".
- **Prefer fewer moving parts** for Brand new users. One platform covering database + login beats stitching three together.
- **Recommend one.** Don't leave them with a survey.
- **Quote the profile, don't extend it.** "Fits you because" should point to what the profile actually says. Don't invent plans ("you'll add logins later") from it. If a future plan would change the recommendation, ask in one line.

## Starting points by tier

Starting points, not answers. Adjust to the rest of the profile and the stack already in the project. If the project already uses a service, prefer extending it over adding a new one.

| Need | T0 (local) | T1 (shared, low stakes) | T2 (public / personal data) | T3 (money / sensitive) |
|---|---|---|---|---|
| Store data | JSON/CSV file, SQLite | SQLite, Supabase or Firebase free tier | Supabase (Postgres + RLS), Firebase with security rules, Neon | Same as T2 + backups turned on |
| Logins | Usually none | Hosted auth (Supabase Auth, Clerk) | Hosted auth. Never hand-rolled passwords | Hosted auth + email verification, rate limits |
| Hosting | None, runs locally | Vercel / Netlify / Cloudflare free tiers | Same, with spending limits set | Same + error monitoring |
| Email | None | Provider free tier | Resend / Postmark with own domain and DNS records (SPF, DKIM) | Same |
| Payments | n/a | n/a | n/a (moves to T3) | Stripe Checkout (hosted payment page) |
| AI / LLM API | Their own key, local only | Key on server only, monthly limit | + per-user caps | + per-user caps and usage logging |

Why these defaults:
- **Supabase** often wins for beginners at T2: database + login + access rules in one place, plain Postgres underneath, so it's easy to leave. Its catch is that RLS must be set up correctly. That's a tripwire, not a reason to avoid it.
- **Firebase** charges per read and write. Fine at small scale, but a loop bug can cost money. Its data model also makes it harder to leave.
- **Stripe Checkout** sends users to a page Stripe hosts, so card details never touch their app. That's the safest option for beginners.

## After they choose

Note the choice under **Notes** in `.vibe/profile.md` (dated, one line). Then build it, applying any tripwires the choice triggers.
