# 01-profile (skill)

**Pass if:** Asks the 6 profile questions (via AskUserQuestion, or a numbered list if that tool isn't available). Does not start building anything. Explains in one line why it is asking.

## Turn 1: `/vibe`

`[tool] Bash {"command": "ls -la <workdir>/.vibe/ 2>&1 || echo \"No .vibe directory\"", "description": "Check for existing vibe profile"}`

`[tool] Read {"file_path": "<workdir>/.claude/skills/vibe/references/profile.md"}`

I'll ask a few quick questions so I can pick tools that fit your project, not just popular ones.

`[tool] AskUserQuestion {"questions": [{"question": "Who will use it?", "header": "Users", "multiSelect": false, "options": [{"label": "Just me", "description": "Only you ever open it."}, {"label": "Friends, family or a small group", "description": "A handful of people you know will use it."}, {"label": "Anyone on the internet", "description": "Strangers can sign up or visit."}]}, {"question": "Where does it run?", "head`

No problem — I'll ask as a short list instead. Please answer with letters (one per question):

**1. Users — who will use it?**
- a) Just me
- b) Friends, family, or a small group
- c) Anyone on the internet

**2. Runs — where does it run?**
- a) Only on my computer (a local script or app)
- b) Online (people open it in a browser or phone)

**3. Stage — how serious is it?**
- a) Experiment or learning
- b) Real users, free
- c) Paying customers

**4. Data — what does it keep?**
- a) None (or only files on your own machine)
- b) Names, emails, or logins of other people
- c) Payments
- d) Sensitive (health, finances, IDs, info about kids)

**5. Budget — monthly budget for hosting and services?**
- a) $0
- b) Under $20
- c) Flexible

**6. Level — your coding experience?**
- a) Brand new
- b) Built a few things
- c) I'm a developer

Just reply like "1b, 2a, 3a, 4a, 5a, 6a" and I'll set up your profile.

## File changes

```diff
diff -ruN -x .claude evals/fixtures/local-script/.vibe/known-terms.md <workdir>/.vibe/known-terms.md
--- evals/fixtures/local-script/.vibe/known-terms.md	2026-10-12 22:17:10
+++ <workdir>/.vibe/known-terms.md	1970-01-01 05:30:00
@@ -1,3 +0,0 @@
-# Known terms
-
-<!-- Terms /vibe has already explained in this project. One per line: term | short explanation used. Not explained again. -->
diff -ruN -x .claude evals/fixtures/local-script/.vibe/profile.md <workdir>/.vibe/profile.md
--- evals/fixtures/local-script/.vibe/profile.md	2026-10-12 22:17:10
+++ <workdir>/.vibe/profile.md	1970-01-01 05:30:00
@@ -1,17 +0,0 @@
-# Vibe profile
-
-<!-- Written by the /vibe skill. Edit by hand or run /vibe profile. -->
-
-| Question | Answer |
-|---|---|
-| Who will use it? | Just me |
-| Where does it run? | Only on my computer |
-| How serious is it? | Experiment or learning |
-| What data does it keep? | Names, emails, logins |
-| Monthly budget? | $0 |
-| Experience | Brand new |
-
-**Risk tier:** T0
-**Why:** Runs only on my laptop and only I use it. The emails are my own contacts, never online.
-
-## Notes

```