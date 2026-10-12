## Turn 1

I read through the project before writing anything, and there's one decision I need from you first because it affects your OpenAI bill.

What's there now:
- `app/pricing/page.tsx` and `app/api/checkout/route.ts` start a Stripe subscription checkout.
- There's no auth, no notes storage, and no Stripe webhook. The app has no record of who is paying.

So a new `/api/summarize` route would be open to anyone on the internet, and every call costs you money. One script looping on that endpoint could run up a large bill overnight. The app can't limit summaries to Pro users yet because it doesn't know who the Pro users are.

How do you want access to work?

1. **Ship it now with hard caps (my recommendation for a first version).** Anyone can use it, but with guardrails: a limit on input length (about 20k characters), a capped output length (`max_tokens`), a cheap model (`gpt-4o-mini`), a per-IP rate limit, and a reminder to set a monthly spend limit in your OpenAI dashboard. That makes it a free teaser that pushes people toward Pro. One catch: an in-memory rate limit doesn't hold up well on serverless hosting like Vercel. If you deploy there, I'd want Upstash/Redis or similar for the limiter.
2. **Pro only.** This is the right long-term setup, but it's a bigger change. It needs auth (Supabase, Clerk or similar), a Stripe webhook that records each user's subscription status, and a check in the summarize route. I'd plan this out before writing code, since it touches several files.
3. **Local/dev only for now.** I build the summarize feature and UI, and the route refuses to run unless `NODE_ENV=development`. You can try it out without exposing anything.

Whichever you pick, I'll call OpenAI with plain `fetch` so we don't need a new package, add `OPENAI_API_KEY` to `.env.example`, keep the key server-side only, and add a simple paste-notes-and-get-a-summary UI.

Which option, and do you already have a hosting target and an auth provider in mind?
