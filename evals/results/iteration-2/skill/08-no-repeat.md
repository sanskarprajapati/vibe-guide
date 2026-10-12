## Turn 1

Using your profile: public waitlist page that stores emails, tier T2.

An **API route** (a small piece of your app that runs on the server, not in the visitor's browser) is the part of your app that does work behind the scenes. Your project already has one: `app/api/signup/route.ts`.

Think of your waitlist like a shop. The page people see (`app/page.tsx`) is the shop counter. The API route is the back room. Visitors can talk to the counter, but they can't walk into the back room. Things that need to stay private, like saving emails or using passwords for other services, happen in the back room.

Here's what happens today when someone joins your waitlist:

1. They type their email and click "Join waitlist".
2. Their browser sends a **request** (a message one computer sends another asking it to do something) to `/api/signup`, with the email inside.
3. Your API route runs on the **server** (a computer online that runs your app's behind-the-scenes code; visitors can't see inside it). It reads the email and replies "ok".
4. The page shows "You're on the list."

One thing to know: the route doesn't save the email anywhere yet. There's a note in the code that says "TODO: store the email somewhere". Right now it only prints the email to a log and then forgets it. So anyone who signs up today is lost. Nothing on the page tells you this, because the visitor still sees "You're on the list."

I didn't change any code. When you're ready, the next step is choosing where the emails get saved. I can walk you through the options.

## Turn 2

Short version: the API route hands the email to a **database** (an organized place to keep information so it's still there tomorrow), and the database keeps it.

```
 Visitor's browser ──(email)──▶ Your API route ──(save)──▶ Database
        ▲                                                     │
        └────────────────("You're on the list")───────────────┘
```

Step by step, once it's set up:

1. **The database gets a place for signups.** Picture a spreadsheet with one row per person: a column for the email and one for when they signed up.
2. **The API route gets permission to write to it.** The database service gives you a **secret key** (a password your app uses to talk to a service; whoever has it gets full access). It lives in a settings file on the server, never in the page code, so visitors can't see it.
3. **The API route adds a row.** When an email arrives, the route checks it looks like a real email, then tells the database "add this row". That replaces the line that prints the email and forgets it.
4. **It answers the browser.** Only after the save works does it reply "ok". If the save fails, it replies with an error, so the page can say "something went wrong, try again" instead of pretending it worked.

Since strangers' emails would be stored, two things come with this when we build it:

- **Lock down who can read the list.** The database needs rules saying visitors can add their own email but can't read anyone else's. Without those rules the page still works perfectly, but a stranger could download your whole list.
- **Keep the secret key off the page and out of GitHub.** If it leaks, anyone can read or wipe the database.

I'd handle both and show you how to check them.

**Where to save it:** for a public page with emails on a small budget, my usual starting point is Supabase (a hosted database with built-in access rules). It has a free tier and keeps things in one place. There are other good options too. When you're ready to build this, say so and I'll lay out two or three choices side by side so you can pick.

I didn't change any code.
