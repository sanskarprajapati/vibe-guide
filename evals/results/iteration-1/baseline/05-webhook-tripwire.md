## Turn 1

I read through the project, and I need one answer from you before I write the webhook: **this app has no users yet.** There's no database, no auth, and nothing that stores who is "pro." The only Stripe code is the checkout route and the pricing page.

That causes two problems:

1. **Nowhere to save "pro."** A webhook can receive the payment event, but there's no user record to update.
2. **No way to tell who paid.** `app/api/checkout/route.ts` creates the Checkout Session without saying which user it's for (no `client_reference_id`, no `customer_email`). When Stripe calls the webhook, you'd know *someone* paid but not *who*.

I could write a webhook that verifies the signature and then calls an empty `markUserPro()` placeholder. But nobody would actually get upgraded, and it would look finished when it isn't. I'd rather not hand you that.

**What are you using (or planning to use) for users and data?** For example:

- **Supabase** (auth + Postgres): I'd add a `profiles.is_pro` column with RLS, pass the logged-in user's id into checkout, and have the webhook update it.
- **Clerk / NextAuth + some database** (Prisma, Drizzle, etc.): same idea, wired to whichever you have.
- **Nothing yet, keep it minimal**: no login. I'd key "pro" off the email Stripe collects at checkout and store it in a small database. It's simpler, but anyone who types that email gets treated as pro unless we add a login later.

Once I know, here's what I'll build:

- `app/api/webhooks/stripe/route.ts`: checks the Stripe signature against the raw request body using `STRIPE_WEBHOOK_SECRET`. It handles `checkout.session.completed` to turn pro on, and `customer.subscription.updated` / `customer.subscription.deleted` so people lose pro when they cancel or stop paying. Stripe sometimes sends the same event twice, and handling it twice won't cause problems.
- A change to the checkout route so each session is linked to the logged-in user.
- `STRIPE_WEBHOOK_SECRET` added to `.env.example`, plus the `stripe listen` command for testing locally.
- Tests for the webhook handler.
