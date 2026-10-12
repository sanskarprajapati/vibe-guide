## Turn 1

Using your profile: public paid SaaS on Stripe, developer, tier T3.
Type /vibe at the start of each session to keep this mode on.

I looked at what's there now. Checkout creates a subscription, but it isn't linked to any user, and `success_url` sends people straight to `/dashboard`. So there's nothing to gate on yet. You'll need two things: an auth provider, and somewhere to store "this user has an active subscription", updated by a Stripe webhook. Nothing hosted exists in the repo yet, so this is the first service decision.

You need logins plus a per-user subscription flag. For a public $9/month SaaS on a budget under $20, these fit:

1. **Clerk**, recommended
   Fits you because: it's the fewest moving parts. Hosted auth with Next.js middleware, and the webhook can write `subscriptionStatus` into the user's `publicMetadata`, so you don't need a database yet.
   Cost at your size: free tier until a fairly large monthly active user count, then per-user pricing. Check current numbers.
   Watch out for: user records live in Clerk. You can export them, but moving off later means a user migration. Metadata also stops working well once you need real relational data, like saved notes per user.

2. **Supabase (Auth + Postgres)**
   Fits you because: you get auth and a real database in one place. A `subscriptions` table keyed to `auth.uid()` with RLS is a clean fit if NoteSnap will save notes per user. It's plain Postgres, so it's easy to leave.
   Cost at your size: the free tier works for building, but free projects pause after inactivity. For paying customers you'd want the paid plan, which also gets you backups. Check current pricing, because it may push you past $20.
   Watch out for: RLS has to be right on every table. That's an extra surface to get wrong.

3. **Auth.js + your own DB, or hand-rolled sessions**: not a fit right now. Auth.js means picking and running a database, adapters and an email provider for magic links. Hand-rolled password storage isn't worth the risk at T3.

Whichever you pick, here's what I'll build, so you can veto anything now:
- Server-side gate on `/dashboard`: middleware plus a check in the page or layout. Hiding the link doesn't stop anyone loading the route directly.
- `/api/checkout` requires a signed-in user and passes `client_reference_id` (and the customer email) to Stripe. The success redirect never grants access by itself.
- A `/api/stripe/webhook` route that handles `checkout.session.completed`, `customer.subscription.updated` and `customer.subscription.deleted`, so cancellations and failed renewals revoke access.

⚠️ Heads up: the webhook is a public URL that decides who gets paid access.
What could go wrong: without signature verification, anyone can POST a fake "payment succeeded" and get Pro for free.
How you'd notice: you wouldn't, until revenue and active users stop matching.
What I'm doing: `stripe.webhooks.constructEvent` on the raw body, with `STRIPE_WEBHOOK_SECRET` kept only in server env. Built and tested in Stripe test mode first.

Since this takes real money, have someone experienced review the auth and webhook code before you go live.

Which one: Clerk (recommended), Supabase, or something else? Also, will NoteSnap store users' notes? If yes, that pushes me toward Supabase.
