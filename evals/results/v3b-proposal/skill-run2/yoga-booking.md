# yoga-booking (skill)

**Persona:** You teach 5 small yoga classes a week (max 12 people each) and currently take bookings over text messages, which is chaos. You're not technical at all. You want students to see the schedule and book a spot. Some students pay per class, some have a 10-class pass, but you're not sure if the site should handle money. Short friendly messages.

## Turn 1

**User:** /vibe I teach yoga classes and want a page where people can book a spot in my classes

`[tool] Bash {"command": "ls -la <workdir> 2>&1; echo \"---\"; ls -la <workdir> 2>&1", "description": "Check project folder and .vibe directory"}`

`[tool] Read {"file_path": "<workdir>"}`

Empty folder, so we're starting fresh. Lovely idea — a booking page for your yoga classes. Let me ask one question at a time so you get to shape it as we go.

First thing that decides most of the rest: **what do your classes look like?** Whether it's a regular weekly rhythm or one-offs changes how the page is laid out and what people see when they open it.

`[tool] ToolSearch {"query": "select:AskUserQuestion", "max_results": 1}`

`[tool] AskUserQuestion {"questions": [{"question": "What do your yoga classes look like?", "header": "Class format", "multiSelect": false, "options": [{"label": "Weekly schedule (Recommended)", "description": "You teach the same classes every week (e.g. Mon 7am, Wed 6pm). The page shows a repeating schedule people book into. Simplest for regulars."}, {"label": "One-off classes", "description": "You add each class when y`

I'll ask it in plain text instead.

What do your yoga classes look like? This decides the whole shape of the page.

a. **Weekly schedule** — same classes every week (Mon 7am, Wed 6pm, etc.). The page shows a repeating weekly rhythm. Simplest if you have regulars. *(my pick)*

b. **One-off classes** — you add each class when you plan it. The page shows a list of upcoming dates. Good if your schedule changes a lot or you mostly run workshops.

c. **A mix of both** — a weekly rhythm plus occasional one-offs. More flexible, a bit more to manage.

_words: 170 · questions: 1 · files changed: 0 _

## Turn 2

**User:** a — weekly schedule works best. same 5 classes every week, pretty regular.

Good — a weekly rhythm. The page will show your 5 classes repeating each week, and people pick one to book.

Next big thing that shapes a lot: **do people pay when they book, or just reserve a spot?** This decides whether we need a payment service (and whether anything costs you money to run).

a. **Free to reserve, pay at class** (cash/Venmo/whatever). Simplest. You can always add online payment later. *(my pick for starting out)*

b. **Pay online when booking** — card payment through something like Stripe. More trustworthy for drop-ins, fewer no-shows, but adds a signup and takes a small cut per booking (~2.9% + 30¢).

c. **Members only** — people have already paid elsewhere (a package, subscription), so booking is just claiming a spot. Needs some way to check they're a member.

_words: 135 · questions: 1 · files changed: 0 _

## Turn 3

**User:** Let's do a. for now, way simpler. Can we also show how many spots are left so people know if it's filling up?

Nice — simplest path, and showing "3 spots left" is a lovely little nudge. Also a nice side effect: once a class fills up, the button changes to "Waitlist" or "Full" so nobody double-books.

To show spots-left, we need to know the max per class. **How big are your classes?**

a. **About the same for all 5** — most teachers have one room/mat setup. Tell me a number (12? 15? 20?) and I'll use it for all five.

b. **Different per class** — e.g. a gentle class holds 8, a power class holds 15. More realistic for some teachers; just means a bit more to set up.

(If you're not sure yet, pick a and we can tweak the number any time.)

_words: 122 · questions: 2 · files changed: 0 _

## Turn 4

**User:** a — all my classes cap at 12.

12 across the board, clean. One more thing that shapes what the booking confirmation looks like: **where do your classes happen?**

a. **In person**, same studio/space. The page shows your address; the confirmation reminds people where to come.

b. **Online** via Zoom (or similar). The confirmation includes the meeting link — only sent to people who booked, so it's not public.

c. **A mix** — some in-person, some online. The page shows which is which per class.

_words: 77 · questions: 1 · files changed: 0 _

## Turn 5

**User:** All in person, same little studio. Address can be public, that's fine.

Perfect, I think I have enough to pitch what we're building. Here's the full picture:

**How it'll work when it's done:**
1. Someone opens your page — sees your 5 weekly classes with times, studio address, and "4 spots left" on each.
2. They tap a class, type their name and email, hit Book.
3. They get a confirmation email: time, address, and a "can't make it?" link.
4. You open a private page any time to see who's booked which class this week.

**What's in front, what's behind:**
- **What people see** (the front end): your public booking page, plus a private admin page just for you.
- **Behind the scenes** (the back end): a small online **database** (a place on the internet that stores bookings so they're shared across everyone's phones), and a tiny **email sender** (a service that sends the confirmation on your behalf). Both have free tiers that cover your size easily — nothing costs you money to run at this scale.

**Features I'd suggest** (pick any, or none):
- **Cancel link in the confirmation email** — one tap frees up the spot for someone else. *(I'd do this first; nothing worse than ghost bookings holding a spot.)*
- **A reminder email the morning of class** — cuts no-shows a lot.
- **Minimum notice (e.g. no booking less than 2hr before)** — stops someone booking as you're already teaching.
- **Optional "first time? injury?" note on the booking form** — helps you prep.

Which do you want in? (pick as many as you like)

_words: 258 · questions: 2 · files changed: 0 _

## Turn 6

**User:** Oh yes please to the cancel link and the reminder email - those two sound amazing! The 2 hour notice thing is smart too, let's add that. And yeah a little note box would be really helpful for new folks.

Lovely — all four it is. Here's how I'd build it, in **6 small steps**:

1. **The public page** — your 5 classes with times, address, a "Book" button that opens a form (name, email, optional note). Looks right, but doesn't save anywhere yet. ← we start here
2. **Make bookings real** — set up the online database, hook up Book so it saves, "spots left" turns real, class flips to "Full" at 12, and the 2-hour rule blocks last-minute bookings.
3. **Confirmation email** — including the cancel link that frees the spot.
4. **Morning-of reminder email** — needs a tiny scheduled job that runs daily and emails whoever has class that day.
5. **Your private admin page** — see this week's bookings by class, with notes from first-timers.
6. **Put it online** so people can visit the real link.

**Why this way:** we build what you can see first, then the plumbing underneath, then the two emails one at a time, then your view, then live. Each step is small enough to try before going on.

**Worth knowing:**
- Steps 2–4 need you to make two free accounts (one for the database, one for the email sender) and paste a couple of codes into a settings file. I'll walk you through; I never see those codes.
- Once we're sending real emails, I'll have you test with your own address first before anything goes to a real person.

Start with step 1?

_words: 243 · questions: 1 · files changed: 0 _

## Turn 7

**User:** Yes please, let's start!

Here we go. Building step 1 — just the look and feel, nothing saves yet. I'll use placeholder class names and address so you can see it; swapping those in is a one-line edit each.

`[tool] Write {"file_path": "<workdir>", "content": "<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />\n  <title>Yoga with [Your Name] \u2014 Book a class</title>\n  <style>\n    :root {\n      --bg: #f6f2ec;\n      --card: #ffffff;\n    `

**Step 1 done: the booking page.**

**Try it:** double-click `index.html` (it'll open in your browser). You'll see 5 placeholder classes with "spots left" counts, and a nearly-full "Power" class in warning orange. Tap **Book** on any class — a form slides up for name, email, and the optional note. Submitting shows a cheerful confirmation (which is fake for now — nothing's saved).

**The idea:** this is just the **front end** (the part people see in their browser). Everything happens inside your browser — refresh the page and any "booking" vanishes. That's fine for shaping how it looks. In step 2 we add the **back end** (the online database where real bookings get saved and shared between visitors).

Two small things worth knowing:
- Colours are a soft sage/cream for now — easy to change later if you want something different.
- "Spots left" turns a warm orange when 3 or fewer are left, as a gentle "last chance" cue.

Before step 2, **what are your 5 classes and your studio address?** Give me each as day + time + name (e.g. "Tuesday 6:30pm — Candlelight Yin"), and I'll swap the placeholders. If you want to tweak the colours or wording too, now's a good time.

_words: 240 · questions: 0 · files changed: 1 ['index.html']_

## Turn 8

**User:** Oh wow this looks really nice! I opened it and the orange on the Power class really does catch my eye, love that.

Here's my 5:
- Monday 9:30am — Morning Flow
- Tuesday 6pm — Slow Flow
- Wednesday 9:30am — Gentle Yoga
- Thursday 6pm — Candlelight Yin
- Saturday 10am — Weekend Flow

Studio is 24 Willow Lane, Suite B. Colors are lovely, don't change a thing!

Lovely list — Candlelight Yin on Thursdays sounds dreamy. Swapping those in now.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "      <span class=\"address\">\ud83d\udccd [Your studio address]</span>", "new_string": "      <span class=\"address\">\ud83d\udccd 24 Willow Lane, Suite B</span>"}`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "    const classes = [\n      { id: \"mon-7\",  day: \"Monday\",    time: \"7:00 am\",  name: \"Gentle Flow\",    spotsLeft: 11 },\n      { id: \"tue-18\", day: \"Tuesday\",   time: \"6:30 pm\",  name: \"Vinyasa\",        spotsLeft: 8  },\n      { id: \"wed-7\",`

Refresh `index.html` — your real classes are in, address is set.

(I left **"Yoga with [Your Name]"** in the big header as a placeholder — just tell me what to put there whenever, or your studio name if you have one.)

Now, step 2: **make bookings real.** Before I start, one choice that decides where your bookings live. This is the one place where you'll need to make a free account somewhere — I'll walk you through it, and I never see your login or any secret codes.

a. **Supabase** — a hosted database (a place on the internet that stores structured data, with a nice table viewer so you can peek at your bookings anytime). Free tier covers you by miles. It's what most small apps use, and it'll make the email features in steps 3–4 much simpler. *(my pick)*

b. **Google Sheets** — your bookings land in a real spreadsheet in your Google Drive, and you see them like any other sheet. Charming, but gets fiddly when two people book at the exact same moment, and the cancel-link feature in step 3 becomes much more awkward.

Which feels better?

_words: 204 · questions: 1 · files changed: 1 ['index.html']_

## Metrics

| Turn | Words | Questions | Files changed | Proposal |
|---|---|---|---|---|
| 1 | 170 | 1 | 0 |  |
| 2 | 135 | 1 | 0 |  |
| 3 | 122 | 2 | 0 |  |
| 4 | 77 | 1 | 0 |  |
| 5 | 258 | 2 | 0 | yes |
| 6 | 243 | 1 | 0 |  |
| 7 | 240 | 0 | 1 |  |
| 8 | 204 | 1 | 1 |  |

- Turns: 8
- First file change on turn: 7
- Most files changed in one turn: 1
- Proposal (how it works, front/back, suggested features) on turn: 5 (before first code change)
- Turns asking more than one question: 2
- Turns ending with no question: 1
- Average words per turn: 181
