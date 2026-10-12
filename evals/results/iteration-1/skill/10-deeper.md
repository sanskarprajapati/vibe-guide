## Turn 1

Using your profile: a contact cleaner that runs only on your laptop, tier T0.
Type /vibe at the start of each session to keep this mode on.

An API (the agreed way one program asks another for something and gets an answer back) is how two programs talk to each other.

Think of ordering at a restaurant counter. You don't walk into the kitchen and cook. You pick from the menu, say your order at the counter, and food comes back. The menu tells you what you can ask for and how to ask. The kitchen stays out of sight. An API is that menu and counter, but for programs: one program sends a request in the agreed format, the other does the work and sends an answer back.

**In your project:** `clean.py` doesn't use an API right now. It reads `contacts.csv` from your laptop, tidies the rows and prints them. Everything happens on your computer, so it has nobody to ask.

**Where one would come in:** say you wanted to check whether each email in your list really exists. Your script can't know that by itself. A company that offers email checking would have an API: your script sends "is asha@example.com real?" and gets back "yes" or "no". Same idea when an app shows the weather (it asks a weather service) or has a "Log in with Google" button (it asks Google).

Worth knowing for later: most APIs need an API key (a password for your program, so the service knows who is asking), and some charge per request. Your project doesn't need any of that now, and I'll flag it before we ever add one.

## Turn 2

Let me draw it instead, using the same email-checking example.

```
  Your script  ──("is asha@example.com real?")──▶  Email-checking company
  (clean.py,                                        (their program, on
   your laptop)                                      their computer)
       ▲                                                   │
       └───────────────────("yes, it's real")──────────────┘
```

The two boxes are two separate programs, often on two different computers. The API is the arrows: the agreed wording your script has to use when it asks, and the agreed shape the answer comes back in. If your script asks in the wrong format, the other side doesn't understand it, the same way a waiter can't take an order for something that isn't on the menu.

Here is your script as it is today, for comparison:

```
  contacts.csv  ──(rows)──▶  clean.py  ──(tidy rows)──▶  your screen
```

Everything stays on your laptop. Nothing goes out to another program and nothing comes back, so there's no API in it.

If it still doesn't click, tell me which part feels fuzzy: why two programs would need to talk at all, what actually gets sent, or where the other program lives. I'll start from that part.
