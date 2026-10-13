# Project profile

Six facts about the project decide which tools fit and which risks matter. **Work out as many as you can from the project before asking anything.** A wall of questions before any help feels like a form, and most answers are already in the code.

## Infer first

| Fact | Where to look |
|---|---|
| Runs | Is it a web app (Next.js, Vite, Express, a `deploy` script, a Vercel/Netlify config) or a local script? |
| Users | Signup or login code, a landing page, "waitlist" or "pricing" in the README → other people use it |
| Stage | Payment code (Stripe, RevenueCat), a pricing page → paying customers |
| Data | Forms collecting email, auth code, payments, anything health/finance/ID-related |
| Budget | Can't be inferred. Assume **$0** until told otherwise, and say so |
| Level | Can't be inferred reliably. Assume **Brand new** until told otherwise; drop explanations if they say they're a developer |

Write the profile with inferred answers marked "(guessed)". Show it in one line in your first brief ("I'm assuming: public site, collects emails, $0 budget, new to coding. Tell me if any of that's wrong.").

**Only ask when the answer changes the plan in front of you**, at most two questions, inside the brief. Budget matters for choosing a paid service; level rarely needs asking. For a small task, don't ask anything: assume the safer answer.

When guessing between two tiers, pick the higher one. Over-warning a hobby project costs a sentence; under-warning a public one can leak data.

## The questions (when you do need to ask)

Ask with `AskUserQuestion`, or a numbered list if it isn't available. Multiple choice; the user can always answer in their own words. `/vibe profile` goes through all six.

| # | Header | Question | Options |
|---|---|---|---|
| 1 | Users | Who will use it? | Just me · Friends, family or a small group · Anyone on the internet |
| 2 | Runs | Where does it run? | Only on my computer · Online (a website or app other people open) |
| 3 | Stage | How serious is it? | Experiment or learning · Real users, free · Paying customers |
| 4 | Data | What data does it keep? | None · Names, emails or logins · Payments · Sensitive (health, finances, IDs, kids) |
| 5 | Budget | Monthly budget for hosting and services? | $0 · Under $20 · Flexible |
| 6 | Level | Your coding experience? | Brand new · Built a few things · I'm a developer |

Add a one-line description under each option so a beginner can choose. For example, under "Online": "people open it in a browser or on their phone, from anywhere."

If the answers to 1 and 2 conflict (anyone on the internet, but runs only on my computer), ask one follow-up instead of guessing.

## Working out the risk tier

Pick the **highest** tier any answer points to.

| Tier | Meaning | Triggered by |
|---|---|---|
| **T0** | Local and private | Just me + only on my computer |
| **T1** | Shared, low stakes | Friends/small group, or online with no personal data |
| **T2** | Public or personal data | Anyone on the internet, or stores names/emails/logins of other people |
| **T3** | Money or sensitive data | Paying customers, payments, or sensitive data |

Edge cases:
- Personal data that is only the user's own and never leaves their laptop (their own contacts in a local CSV) stays T0. Note it in the profile; it matters if they ever deploy.
- "Experiment" with payments is still T3. Payment mistakes cost real money even in experiments, unless they're using Stripe's test mode only. Then note "test mode only" and use T2 until they go live.

Write a one-line **Why** in the profile in plain words: "Public page that stores strangers' email addresses."

## What each tier changes

| | T0 | T1 | T2 | T3 |
|---|---|---|---|---|
| Default tools | Local files, SQLite, no hosting | Free tiers, simple hosting | Managed services with built-in auth and access rules | Same as T2, plus backups and monitoring |
| Tripwires | Secrets only | + cost, deploys | All except payments/sensitive | All |
| Decision cards | Only if they ask for a hosted service | For any hosted service | For any service | For any service, with "before launch" notes |
| Extra | Keep it simple | Billing alerts | Access rules from day one | Recommend a human review before launch |

Budget and level filter further:
- **$0:** never recommend something without a usable free tier. Say where the free tier ends.
- **Under $20:** prefer predictable flat pricing over pay-per-use where the choice is close.
- **Brand new:** fewer moving parts. One platform that does database + auth beats three separate services.
- **Developer:** explanations off; still use cards and tripwires, in short form.

## Keeping it current

When the user says something that changes the profile ("my friends want to use it too", "I want to charge for it"), say what changed and offer to update the file. Update the tier and add a dated line under **Notes**. Don't silently change it.
