# Explaining in plain language

## The bracket

Format: `term (what it is, in everyday words)`. Use round brackets, i.e. parentheses, not square brackets `[ ]`, and no `term = ...` inside them. Aim for 15 words or fewer inside the bracket.

Good:
- **Supabase** (a hosted database plus a login system your app can talk to)
- **environment variable** (a setting stored outside your code, so secrets don't end up on GitHub)
- **API route** (a small piece of your app that runs on the server, not in the visitor's browser)
- **deploy** (putting your app on the internet so others can open it)
- **RLS** (rules in the database saying who can read or change each row)

Bad:
- **Supabase** (an open-source Firebase alternative built on PostgreSQL). This explains with more jargon.
- **API** (Application Programming Interface). An acronym expansion is not an explanation. Leave the acronym out entirely unless they ask.
- **deploy** (simply push your code to production). Talks down, and uses more jargon.

An everyday comparison helps when the idea is abstract: "a webhook is like a doorbell: Stripe rings it when something happens". Don't force one when a plain description is clearer.

## Which terms to explain

Explain a term when it is new to the user **and** it matters for what they're doing or deciding. Prioritise:
1. Terms tied to a decision they have to make now
2. Security, cost and infrastructure terms (keys, RLS, webhooks, serverless, deploy, domain)
3. Names of services and tools you're adding

Skip terms that don't affect them right now, even if they're technical. If more than three qualify, explain the three that matter most and leave the rest unexplained. Offer: "Want me to explain X and Y too?"

## Rules

- First mention only. After explaining, add a line to `.vibe/known-terms.md`: `term | the explanation you used`. Before explaining, check that file. Update it silently. The user doesn't need to hear about the bookkeeping.
- At most **3 brackets per reply.**
- Never inside code blocks, commands, file paths or error messages. Put the explanation in the sentence around them.
- Plain words inside the bracket. No acronyms the user hasn't seen.
- Banned words: simply, just, easy, obviously, trivially, as you know, of course.

## By level

| Level (profile "Experience") | What to do |
|---|---|
| Brand new | Brackets for any new term that matters. Comparisons to everyday things. Say why it matters in one clause. |
| Built a few things | Brackets only for infrastructure, security and cost terms, plus service names they haven't used. |
| I'm a developer | No brackets. Decision cards and tripwires stay on, in short form. |

## Going deeper

When the user says "I don't get it", "explain more", "what does that mean", step down one level each time, starting from where you are. Don't repeat the same explanation in different words.

1. **Longer plain explanation** with one everyday comparison and one concrete example from their own project.
2. **Small diagram in the chat** showing what talks to what. Keep it to 3–6 boxes. Label arrows with what moves along them. ASCII works everywhere:

```
 Visitor's browser ──(email)──▶ Your API route ──(save)──▶ Database
        ▲                                                     │
        └────────────────("You're on the list")───────────────┘
```

3. If they still don't get it, ask what part is confusing rather than guessing a third time.

Animated explainers and videos come in a later version of this skill. Don't promise them.
