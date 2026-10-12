## Turn 1

Using your profile: public waitlist page that stores emails, tier T2.
Type /vibe at the start of each session to keep this mode on.

An **API route** (a small piece of your app that runs on the server, not in the visitor's browser) is the part of your app that does work behind the scenes.

Your Plantpal app has two halves:

- **The page** (`app/page.tsx`) runs in the visitor's browser. It shows the heading, the email box and the "Join waitlist" button.
- **The API route** (`app/api/signup/route.ts`) runs on the **server** (a computer online that runs your app's behind-the-scenes code, out of visitors' sight).

When someone clicks "Join waitlist", the page sends a **request** (a message one program sends another, asking it to do something) to the address `/api/signup`, with the email inside. The API route receives it, does its job, and answers "ok". The page then shows "You're on the list."

Think of it like a restaurant: the page is the dining room where guests fill in the order slip, and the API route is the kitchen. Guests can't walk into the kitchen, so it's where you keep anything private, like passwords to your database.

Right now your API route only prints the email to the server's log and then says "ok". Nothing is saved, so every signup so far would be lost. That's the `TODO` line in the file.

I didn't change any code. Want me to walk through how saving the emails would work next?

## Turn 2

Using your profile: public page, strangers' emails, under $20 a month, tier T2.

The API route stays the middleman. Only one new step goes inside it:

```
 Visitor's browser ──(email)──▶ Your API route ──(save the email)──▶ Database
        ▲                                                               │
        └──────────("You're on the list")◀──────────("saved")───────────┘
```

1. The page sends the email to `/api/signup`, the same as now.
2. The API route checks it looks like a real email address.
3. It connects to the **database** (an organised place online that keeps your data, like a spreadsheet your app can write to) using a secret key that only the server knows.
4. It adds one new row: the email and the time they signed up.
5. Only after the database confirms the save does it answer "ok", so nobody sees "You're on the list" unless their email was actually kept.

Two things matter for a public page like yours, and I'd set both up when we build it:

- The database key lives in a settings file on the server, never in the page code, so visitors and bots can't find it.
- The database gets access rules that let the public **add** an email and nothing else. Without those rules, anyone who found the address could download your whole list of emails. Your page would keep working, so you wouldn't notice.

Before any of that, you need to pick a database. For a public waitlist with a small budget and room to add logins later, here's what fits:

1. **Supabase** (a hosted database plus a login system your app can talk to), recommended
   Fits you because: one service covers saving emails now and user logins later, and it has the "add-only" access rules built in.
   Cost at your size: free tier covers a waitlist comfortably; paid plans are a flat monthly price. Check current pricing.
   Watch out for: the access rules have to be set up correctly. I'll do that and show you where to check them in its dashboard. Your data is in a standard format, so moving away later is straightforward.

2. **Firebase** (Google's hosted database and login service, priced per read and write)
   Fits you because: also covers database and logins in one place, with a free tier.
   Cost at your size: free for a small waitlist, but you pay per read and write, so a bug that loops can cost money. Your budget favours flat pricing.
   Watch out for: its security rules must be written to block everything by default, and its data format makes switching away harder later.

3. **Saving emails to a file on the server**: not a fit for you. Most hosts for apps like yours wipe or don't keep files between visits, so emails would quietly disappear.

Which one?
