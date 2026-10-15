# Tripwires

The dangerous mistakes in vibe-coded apps share one property: the app works fine with or without them. Nothing breaks, nothing turns red. A tripwire makes the invisible risk visible **before** the user agrees to the work, and says what you're doing about it.

## Where it goes

- **In the question or outline where it matters:** one line, with what you'll do: `The email list could be readable by anyone → insert-only access rules, no public reading.` The user hears the risk before agreeing to that step.
- **Mid-build, for a risk nobody discussed:** a checkpoint (see `briefing.md`) if it changes the plan, or the four-line form below if you can handle it safely and keep going.

## Four-line form

```
⚠️ Heads up: <what this is, in one line>
What could go wrong: <concrete consequence, in their terms>
How you'd notice: <usually "you wouldn't, until…">
What I'm doing: <the safe default you're applying>
```

Write it as normal text in the reply, not inside a code block, so the bold and line breaks render. Four lines. If the same tripwire already fired this session, use one line: `⚠️ Same as before: secret key stays on the server.`

At the **I'm a developer** level, always use the one-line form: what the risk is and what you did. `⚠️ Webhook: verifying the Stripe signature on the raw body; signing secret in server env only.` Developers know why it matters; they want to know you handled it.

Never end a tripwire with "you're safe now". Say what you did.

## When each one fires

Fire at the listed tier **and above**. Re-read `.vibe/profile.md` to get the tier.

| Trigger | Tier |
|---|---|
| API key, password or secret going into code, a frontend variable, or git | T0 |
| Adding a pay-per-use service (AI/LLM API, serverless functions, per-read database) | T1 |
| Deploying, or making anything reachable from the internet | T1 |
| Creating database tables, or changing who can read or write them | T2 |
| Login, signup, password reset, sessions | T2 |
| Sending email | T2 |
| Deleting data, migrations that change or drop columns | T2 |
| Payments, webhooks | T3 |
| Storing sensitive data (health, finances, IDs, children) | T3 |

Below the listed tier, apply the safe default silently. Don't warn.

## What to say and do

### Secrets and keys
- **Wrong:** a secret key in code that ships to the browser, or committed to git. Bots scan GitHub and frontend bundles for keys within minutes; someone runs up a bill or reads the database.
- **Safe default:** secrets go in `.env.local` (or the host's environment settings), and `.env*` goes in `.gitignore`. Only use secrets in server code.
- **Frontend prefixes:** anything named `NEXT_PUBLIC_*`, `VITE_*`, `PUBLIC_*`, `EXPO_PUBLIC_*` or `REACT_APP_*` is visible to every visitor. Never put a secret behind those prefixes.
- **Supabase specifically:** the anon / publishable key is *meant* to be public, and it's only safe if RLS is on with correct policies. The `service_role` / secret key skips every rule and must never reach the browser.

### Pay-per-use services
- **Wrong:** a bug in a loop, a page that calls the API on every load, or one abusive user can turn into a large bill overnight.
- **Safe default:** key on the server only. Tell them to set a monthly spending limit and a billing alert in the provider's dashboard. That's a step only they can do, so say exactly where. Add a per-user cap or rate limit in code. Don't call paid APIs on page load.

### Deploying
- **Wrong:** something that was private becomes public: local files, test data, debug pages, open endpoints.
- **Safe default:** list what will become reachable. Check that no secrets or real data files get uploaded (for example, a CSV of real contacts). Make sure environment variables are set on the host, not in code. If the profile said "only on my computer", confirm first and offer to update the profile.

### Database access rules (RLS, security rules)
- **Wrong:** "RLS enabled" with a policy that allows everyone is the same as no RLS. Anyone with the public URL and key can read the whole table. That's how 170+ Lovable apps and Moltbook leaked data.
- **Safe default:** turn on RLS for every table. Write the narrowest policies that work. For a signup form, that's insert-only for anonymous users, with no select. For per-user data, the policy matches `auth.uid()` to an owner column. For Firebase, write security rules that deny by default.
- Tell them how to check it themselves (Supabase dashboard → Authentication → Policies, or the Security Advisor).

### Logins
- **Wrong:** checking permissions only in the screens, not on the server. Hiding a button doesn't stop someone calling the API directly. Hand-rolled password storage.
- **Safe default:** use a hosted auth provider. Check the user on the server for every protected action and route.

### Email
- **Wrong:** default or shared senders land in spam, so users never get their confirmation or password-reset email, and nothing tells you.
- **Safe default:** send from their own domain through a provider (Resend, Postmark), with SPF and DKIM DNS records. Say that the DNS step is theirs, and where to do it.

### Deleting data and migrations
- **Wrong:** a migration that drops or renames a column deletes real data with no undo.
- **Safe default:** say exactly what will be deleted or changed. Back up first, or add the new column before removing the old one. Ask before running anything destructive.

### Payments and webhooks
- **Wrong:** a webhook is a public URL. If it doesn't check that the request really came from Stripe, anyone can send a fake "payment succeeded" and get the paid plan free.
- **Safe default:** verify the signature with `stripe.webhooks.constructEvent(rawBody, signature, secret)` using the **raw** request body. Keep the webhook signing secret in an environment variable. Use Stripe Checkout so card details never touch their app. Build and test in Stripe test mode first.
- At T3, recommend a review by someone experienced before taking real payments.

### Sensitive data
- **Wrong:** health, financial, ID or children's data has legal rules (GDPR, HIPAA, COPPA, depending on where they and their users are) and a leak harms real people.
- **Safe default:** store as little as possible. Lock down access rules. Tell them plainly that this kind of data may carry legal obligations, and that they should check what applies before launch. Don't give legal advice beyond that.
