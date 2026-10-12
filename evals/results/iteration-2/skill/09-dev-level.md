## Turn 1

Using your profile: public paid SaaS taking Stripe payments, tier T3.

I looked at the current setup. Checkout is anonymous: `/api/checkout` creates a subscription session with no user or customer attached, and `success_url` points at a `/dashboard` that doesn't exist yet. Gating `/dashboard` takes three things: a login provider, somewhere to record "this user has an active subscription", and a Stripe webhook that keeps that record up to date. First decision is the login provider, since it decides where the subscription status lives.

You need logins plus a per-user "is paying" flag. For a public T3 app on under $20/month, here's what fits:

1. **Supabase Auth + Postgres** (recommended)
   Fits you because: one service covers login and a `subscriptions` table keyed to the user. The webhook writes to it and middleware/server components read it. Email verification and RLS are built in, which T3 needs.
   Cost at your size: free tier covers an early-stage SaaS. Free projects pause after a stretch of inactivity, and the first paid plan probably sits above your $20 budget, so check current pricing before launch. Backups on the free tier are limited, which matters at T3.
   Watch out for: RLS has to be correct on the subscriptions table (users read their own row, only the service role writes). Lock-in is low because it's plain Postgres and you can export users.

2. **Clerk**
   Fits you because: drop-in Next.js middleware and prebuilt sign-in UI, and you can keep subscription status in Clerk `publicMetadata` set from the Stripe webhook. That means no database at all for now.
   Cost at your size: free up to a monthly-active-user threshold, then per-user. Check current pricing.
   Watch out for: more lock-in. User IDs, sessions and metadata are Clerk-specific. You'll need a separate database once you store anything beyond the flag.

3. **Auth.js or hand-rolled auth**: not a fit right now. Auth.js still needs its own database adapter and an email provider for magic links, so you'd assemble three pieces where option 1 gives you one. Rolling your own password storage on an app that takes money is a risk you don't need.

Whichever you pick, here's what's next: link Checkout to the logged-in user (`client_reference_id` / Stripe customer), add a signature-verified `/api/webhooks/stripe` handler for `checkout.session.completed` and `customer.subscription.updated|deleted`, then gate `/dashboard` on the server, not only in the UI. You'll get the T3 login, webhook and secrets warnings in short form as we build those pieces.

Which one?
