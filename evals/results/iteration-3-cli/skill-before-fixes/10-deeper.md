# 10-deeper (skill)

**Pass if:** Turn 1: plain explanation with an everyday analogy. Turn 2: goes one step deeper with a small diagram (ASCII or mermaid) instead of repeating the same words.

## Turn 1: `/vibe I don't get what an API is`

`[tool] Bash {"command": "ls -la .vibe/ 2>/dev/null && echo \"---\" && cat .vibe/profile.md 2>/dev/null && echo \"---\" && cat .vibe/known-terms.md 2>/dev/null", "description": "Check for existing vibe profile"}`

Using your profile: laptop-only learning project, tier T0.

An **API** is a way for one program to ask another program to do something.

Think of a restaurant. You don't walk into the kitchen and cook. You read the menu, tell the waiter what you want, and they bring it back. The menu + the waiter is the API. The kitchen is the other program doing the actual work.

A real example: when a weather app on your phone shows today's temperature, it isn't measuring the weather itself. It asks a weather service's API: *"what's the temperature in San Francisco?"* The service answers *"62°F"*. The app shows that to you.

So an API is two things bundled together:
- a **list of questions or actions** another program accepts (the menu)
- the **rules for how to ask and what you get back** (how to talk to the waiter)

A few things that trip people up at first:

- You don't see an API — it's not a screen. It's just programs talking to each other in the background.
- The other program can live anywhere: on your own computer, or on a company's server across the internet. Most of the time, "API" means the latter.
- Some APIs are free, some charge per request. That's why you sometimes need an **API key** — a password that says "this request is from me, bill me if needed". Keys are the kind of thing we'd be careful with later; for now just know they exist.

Want me to show you a tiny working example — like a few lines of code that call a real API and get an answer back? Or keep going with words?

`[tool] Write {"file_path": "<workdir>/.vibe/known-terms.md", "content": "# Known terms\n\n<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->\nAPI | a way for one program to ask another program to do something; like a menu + waiter at a restaurant\nAPI key | a p`

`[tool] Read {"file_path": "<workdir>/.vibe/known-terms.md"}`

`[tool] Write {"file_path": "<workdir>/.vibe/known-terms.md", "content": "# Known terms\n\n<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->\nAPI | a way for one program to ask another program to do something; like a menu + waiter at a restaurant\nAPI key | a p`

## Turn 2: `still don't get it`

Okay, let me scrap the restaurant thing and try a different angle.

**An API is just a web address that gives back data instead of a webpage.**

That's really the whole thing.

- You type `google.com` in your browser → you get a **page you can look at**.
- A program sends a request to `api.openweathermap.org/.../sanfrancisco` → it gets back **raw text** like `{"temp": 62, "sky": "clear"}`.

Same internet. Same kind of address. Different kind of answer.

- A **webpage** is for humans to read.
- An **API** is for programs to read.

That's it. Everything else — keys, endpoints, requests, responses — is just details stacked on top of that one idea.

Want to actually see one? Paste this into your browser's address bar and hit enter:

```
https://api.github.com/users/torvalds
```

You'll get back a wall of text with info about Linus Torvalds. That text is an API response. No app, no code — your browser just asked an API a question, and the answer came back.

Does seeing that help? If not, tell me which part is still fuzzy — "I don't know what *data* means", "I don't get what a *program* is here", "I don't get why anyone would want this" — any of those is a fine answer and I'll go from there.

## File changes

```diff
diff -ruN -x .claude evals/fixtures/local-script/.vibe/known-terms.md <workdir>/.vibe/known-terms.md
--- evals/fixtures/local-script/.vibe/known-terms.md	2026-10-12 22:17:10
+++ <workdir>/.vibe/known-terms.md	2026-10-12 22:30:17
@@ -1,3 +1,5 @@
 # Known terms
 
 <!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->
+API | a way for one program to ask another program to do something; like a menu + waiter at a restaurant
+API key | a password that identifies you to an API, so the service knows who's asking and can bill you

```