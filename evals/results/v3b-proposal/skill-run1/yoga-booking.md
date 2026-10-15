# yoga-booking (skill)

**Persona:** You teach 5 small yoga classes a week (max 12 people each) and currently take bookings over text messages, which is chaos. You're not technical at all. You want students to see the schedule and book a spot. Some students pay per class, some have a 10-class pass, but you're not sure if the site should handle money. Short friendly messages.

## Turn 1

**User:** /vibe I teach yoga classes and want a page where people can book a spot in my classes

`[tool] Bash {"command": "ls -la <workdir> 2>&1 | head -40 && echo \"---VIBE---\" && ls -la <workdir> 2>&1", "description": "List project and vibe directories"}`

`[tool] Read {"file_path": "<workdir>"}`

Lovely — a booking page for your classes. Before I plan it, one thing shapes everything else.

**When someone books, do they pay upfront, or just reserve a spot?**

a. **Just reserve.** They pick a class, leave their name and email, and show up. You collect payment at the studio (cash, card reader, whatever you already use). *(my pick to start — simplest, no fees, no bank setup, and you can add payments later)*

b. **Pay upfront per class.** They pay when booking. Needs a payment service (Stripe is the usual one — about 2.9% + 30¢ per booking, and you'll make a free account and paste two keys).

c. **They buy a pack (e.g. 5 classes) and spend one when booking.** Nicer for regulars, but it adds packs, balances, and expiry rules — a bigger build.

Which fits how you work today?

_words: 143 · questions: 1 · files changed: 0 _

## Turn 2

**User:** Let's do (a) just reserve for now. Keeps it simple and I already have a card reader at the studio. Can we maybe add the class pass thing later once this is working?

Reserve-only it is — and yes, class packs can slot in later. We'll store names and emails per class, and when you add payments or packs down the line, we just plug them onto what's already there. No wasted work.

Next thing that shapes the page: **what does your class schedule look like?**

a. **Same classes every week** (e.g. Mon 7am Vinyasa, Wed 6pm Yin, Sat 9am Hatha). People see a weekly timetable, book the next upcoming session of a class. *(my pick if your schedule is steady — easiest to keep tidy)*

b. **A list of specific upcoming classes you post** (e.g. "Vinyasa — Sat 18 Oct 9am"). You add each class with a date and time. More typing for you, but handy if your schedule shifts or you run workshops.

c. **Both** — a regular weekly timetable, plus one-off workshops. Nicer for students, slightly more to build.

Which matches how you teach?

_words: 154 · questions: 1 · files changed: 0 _

## Turn 3

**User:** a — same 5 classes every week, pretty steady. Mon/Tues/Thurs mornings and Wed/Sat evenings if that matters.

Perfect — a steady weekly timetable. People will see all five classes with the next date filled in automatically, so you never have to re-add them. The days of the week don't change the build; I'll ask you to type the exact times and class names when we get there.

Next: **does each class have a limit on how many people can book?**

a. **Yes, a fixed cap per class** (e.g. 12 mats). The page shows "3 spots left" and stops bookings when full. *(my pick — studios almost always need this, and "sold out" is nicer than a double-booking at the door)*

b. **Different cap per class** (e.g. 15 for Vinyasa, 8 for a smaller Yin room). Same as above but you set the number class by class.

c. **No cap, book freely.** Simpler, but you may get more people than you have mats for.

Which fits your studio?

_words: 150 · questions: 1 · files changed: 0 _

## Turn 4

**User:** Yeah option a, 12 mats for every class.

Twelve mats across the board — easy to remember, easy to show "3 of 12 spots left".

Now the one slightly technical choice, because it shapes what you'll set up: **where do the bookings get saved?** Students book from their own phones, so the bookings have to live somewhere online that every phone can reach — not just on your computer.

a. **Supabase** (a free hosted database — a place on the internet that stores a list of bookings). You make a free account, I paste two settings values into a hidden file (you never share them with me, you copy them in yourself). Free tier easily covers a yoga studio. Everything stays in one tidy place. *(my pick — it's the normal choice for this)*

b. **Google Sheets** as the storage. Bookings land as new rows in a spreadsheet you own. Nice if you already live in Sheets and want to eyeball bookings there. Trickier to keep tidy and a bit slower, but no new account.

c. **Airtable.** Like a prettier spreadsheet with a free tier. Good middle ground, but it's another account, and the free tier has lower limits than Supabase.

One thing worth knowing up front: students' names and emails count as personal data, so wherever we store it, I'll keep it to only what's needed (name, email, which class), and I'll never hard-code any secrets into the page itself.

Which do you want?

_words: 237 · questions: 1 · files changed: 0 _

## Turn 5

**User:** Let's go with a, Supabase. I trust your pick, and keeping it all tidy in one place sounds good to me.

Supabase it is. Now I can pitch the whole thing.

**How it'll work when it's done:**
1. A student opens your page on their phone and sees your five weekly classes with the next date for each.
2. They tap a class, see "9 of 12 spots left", type their name and email, and tap Book.
3. The booking lands in your Supabase (your online bookings list) and the page shows "You're in — see you Saturday 9am".
4. You open the same page from a private link and see who's booked for each class.

**What's in front, what's behind:**
- **What people see** (the front end): the timetable page with the five classes, and a small booking form on each.
- **Behind the scenes** (the back end): Supabase holds a list of your classes (name, day, time, cap) and a list of bookings (name, email, which class, which date). The page talks to Supabase directly — no server of yours to run or pay for.

**Features I'd suggest** for a yoga booking page (pick any, or none):
- **Confirmation email to the student**: they get an email with the class name, date, time and address. People forget; this cuts no-shows. *(I'd do this first — students expect it)*
- **Your teacher view**: a private link showing who's booked for each class, so you can scan the roster before you teach.
- **Self-serve cancellation**: a link in the confirmation email lets them cancel their spot, freeing it for someone else — fewer "sorry, can't make it" texts for you.
- **Waitlist when full**: if a class is full, they join a waitlist and get auto-booked if someone cancels. Nicer for regulars, but adds a chunk of work — fine to add later.

Which of these do you want?

_words: 298 · questions: 1 · files changed: 0 _

## Turn 6

**User:** Yes to the confirmation email and the teacher view — those two feel like musts. Skip the cancellation and waitlist for now, let's keep it simple and add later if I need it.

Here's how I'd build it, in 5 small steps:

1. **The timetable page** — five classes with the next date filled in, and a booking form on each. Not saving yet, so you can see the shape.  ← we start here
2. **Hook up Supabase** — bookings actually save, "N of 12 spots left" shows live, and "Sold out" when full.
3. **Confirmation email to the student** — right after they book.
4. **Your teacher view** — a private page listing who's booked for each class.
5. **Put it online** — a real link you can share.

Why this way: each step gives you something you can touch — a page, then a real booking, then an email, then your roster. If anything feels off, we catch it before building the next bit.

Worth knowing up front:
- **Your teacher view will be private by hard-to-guess link, not a password.** Fine if you don't share it; if that worries you, we can add a password at step 4.
- **Sending email needs one more free account** (Resend is the usual, free up to 3,000 emails/month). I'll walk you through it when we get to step 3 — you make the account, I never see the key.
- Before we go online at step 5, I'll check nothing private (your keys, your bookings list) is in the files we publish.

Start with step 1?

_words: 233 · questions: 1 · files changed: 0 _

## Turn 7

**User:** Yes let's start! That plan sounds good to me. The private link for my teacher view is fine for now, I can always add a password later if I get nervous.

`[tool] Write {"file_path": "<workdir>", "content": "<!doctype html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"utf-8\" />\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n  <title>Book a Class</title>\n  <style>\n    :root {\n      --ink: #2b2b2b;\n      --muted: #6b6b6b;\n      --paper: #f6f2ec;\n     `

**Step 1 done: the timetable page.**

**Try it:** double-click `index.html` (it's in the project folder). You'll see five class cards with the next date and time filled in automatically, name/email fields, and a Book button. One class is set as "Sold out" so you can see what that looks like. Clicking Book shows a confirmation on screen, but nothing is saved yet — that's step 2.

**The idea:** right now everything happens inside the one HTML file in your browser. The class list is written at the top of a script block (a short bit of code that runs in the page) — easy to change. The dates aren't typed in; the page works out "next Monday" each time it loads. The sold-out and spots-left bits are placeholders for now so you can feel the shape.

One thing before step 2: I used placeholder class names and times — Vinyasa Flow (Mon 7am), Gentle Hatha (Tue 7am), Yin & Breath (Wed 6pm), Vinyasa Flow (Thu 7am), Restorative (Sat 6pm). **Are those names and times roughly right, or should I use yours?** If you give me the real five (name, day, time), I'll pop them in before we move on.

_words: 199 · questions: 0 · files changed: 1 ['index.html']_

## Turn 8

**User:** opened it and it looks just like you said, the cards and the sold out one. my real ones are: Slow Flow Mon 9am, Beginners Tue 6pm, Flow Wed 9am, Gentle Thu 6pm, Weekend Stretch Sat 8am — can you swap those in?

Swapping those in now.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "    const CLASSES = [\n      { id: \"mon-vinyasa\", name: \"Vinyasa Flow\",   day: 1, hour: 7,  minute: 0,  cap: 12 },\n      { id: \"tue-hatha\",   name: \"Gentle Hatha\",   day: 2, hour: 7,  minute: 0,  cap: 12 },\n      { id: \"wed-yin\",     name: \"Yin & B`

Done — refresh the page in your browser and you'll see your five real classes, with the next date filled in for each.

Now step 2: hooking up Supabase so bookings actually save and the "spots left" count is real, not fake. Before I can do anything on my side, you'll need to make the free account and send me two small values the page uses to talk to your database. I'll walk you through it:

1. Go to **supabase.com**, click **Start your project**, sign in (email or GitHub, your call).
2. Click **New project**. Give it a name like "yoga-bookings", pick any region near you, and let it set a database password — save that somewhere, you won't need it for this build but it's good to keep.
3. Once it finishes setting up (takes about a minute), on the left sidebar click the **gear icon → API** (or **Project Settings → API**).
4. You'll see two things I need: a **Project URL** (looks like `https://xxxx.supabase.co`) and a key labelled **anon public** (a long string of letters and numbers).

Paste both back to me here. **Only the `anon public` key — not the `service_role` one.** The anon key is the one meant to be used from a web page; it's safe for the browser to see because the database rules decide what it's allowed to do (we'll set those up next). The `service_role` key would give full admin access, so we never put it in a page.

Ready to give it a try?

_words: 258 · questions: 1 · files changed: 1 ['index.html']_

## Metrics

| Turn | Words | Questions | Files changed | Proposal |
|---|---|---|---|---|
| 1 | 143 | 1 | 0 |  |
| 2 | 154 | 1 | 0 |  |
| 3 | 150 | 1 | 0 |  |
| 4 | 237 | 1 | 0 |  |
| 5 | 298 | 1 | 0 | yes |
| 6 | 233 | 1 | 0 |  |
| 7 | 199 | 0 | 1 |  |
| 8 | 258 | 1 | 1 |  |

- Turns: 8
- First file change on turn: 7
- Most files changed in one turn: 1
- Proposal (how it works, front/back, suggested features) on turn: 5 (before first code change)
- Turns asking more than one question: 0
- Turns ending with no question: 1
- Average words per turn: 209
