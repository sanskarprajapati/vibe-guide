# bakery-orders (skill)

**Persona:** You run a small home bakery and sell cakes to locals through Instagram DMs today. You've never built a website. You want people to see your cakes and order ahead for pickup. You'd like to take payment if it's not complicated, but you're worried about fees and doing something wrong with card details. Answer in short casual messages.

## Turn 1

**User:** /vibe i want a simple website for my bakery where people can see the menu and order cakes

`[tool] Bash {"command": "ls -la <workdir> 2>&1 | head -30 && echo \"---\" && ls -la <workdir> 2>&1 | head -20", "description": "Check project folder and .vibe profile"}`

`[tool] Read {"file_path": "<workdir>"}`

A bakery website — nice. Let me set up the vibe profile folder and then start the conversation.

`[tool] Bash {"command": "mkdir -p <workdir>", "description": "Create .vibe folder"}`

`[tool] ToolSearch {"query": "select:AskUserQuestion", "max_results": 1}`

A bakery site people can order cakes from — lovely project. Before I build anything, there's one choice that shapes everything else: **how should orders actually reach you?**

`[tool] AskUserQuestion {"questions": [{"question": "When someone orders a cake, how should the order reach you?", "header": "Order flow", "multiSelect": false, "options": [{"label": "Email you the order details (Recommended)", "description": "Customer fills a form (cake, size, pickup date, their phone). You get an email, then confirm by phone or reply. No online payment \u2014 they pay at pickup. Simplest, free to run, `

It looks like the question didn't go through — no worries. Here it is in plain text, pick a letter:

**When someone orders a cake, how should the order reach you?**

a. **Email you the order details** *(my pick)* — customer fills a form (cake, size, pickup date, their phone), you get an email, then confirm by phone or reply. No online payment, they pay at pickup. Simplest, free to run, and you get to double-check tricky custom-cake details before saying yes.

b. **WhatsApp message with the order prefilled** — they tap "Order" and WhatsApp opens with the cake details ready to send to your number. Feels fast and personal, no email needed. Good if WhatsApp is already how your customers reach you.

c. **Full online checkout with card payment** — they pay online with a card. You get the order already paid. More to set up, small fee per order (around 2–3%), and refusing a tricky request after they've paid is awkward. The site also has to be hosted somewhere that costs a bit to run.

Which one feels right for how you work?

_words: 231 · questions: 1 · files changed: 0 _

## Turn 2

**User:** b sounds good — most of my orders already come through DMs so WhatsApp fits how people already reach me

WhatsApp it is — fits how people already reach you, and no email setup needed. The "Order on WhatsApp" button will open with the cake details already written, so they just tap send.

Next thing that shapes the site: **what's actually for sale?**

a. **A fixed menu of cakes with set prices** — e.g. "Chocolate fudge 500g — $25", "Red velvet 1kg — $45". People pick one, tap WhatsApp, done. *(my pick if most of your cakes are the same recipes over and over)*

b. **Custom cakes with choices** — people pick size, flavour, writing on top, pickup date, etc. The WhatsApp message gets built from their choices. Better if every cake is bespoke, but the form is longer.

c. **Both** — a short fixed menu for everyday cakes, plus a "custom order" option for birthdays/weddings. More to build, but closer to how most bakeries actually work.

Which fits your bakery?

_words: 151 · questions: 1 · files changed: 0 _

## Turn 3

**User:** c sounds right - most people want the usual ones but birthdays are always custom with names and stuff

Perfect — fixed menu for regulars, custom form for birthdays. That's exactly how most bakeries actually run.

One more thing before I sketch the whole picture: **do customers pick up, or do you deliver?**

a. **Pickup only** — they come to you. Form asks for pickup date and time. Simplest. *(my pick if you're mostly local word-of-mouth)*

b. **Delivery only** — form asks for their address. You'll want to say which areas you cover somewhere on the page.

c. **Both, customer chooses** — a toggle on the order form. Delivery adds an address field and a note like "delivery fee confirmed on WhatsApp".

Which one?

_words: 105 · questions: 1 · files changed: 0 _

## Turn 4

**User:** pickup only, they come to me. i don't want to mess with delivery right now.

Pickup only, got it. Here's the shape of it:

**How it'll work when it's done:**
1. Someone lands on your page and sees a short welcome + today's menu with photos and prices.
2. They tap a cake, pick a size if there are options, hit "Order on WhatsApp" — their phone opens WhatsApp with the order already written to your number. They just tap send.
3. For birthdays, there's a "Custom cake" button that opens a form: size, flavour, writing on top, pickup date. Submit → same thing, prefilled WhatsApp message to you.
4. You confirm, agree a price, done.

**What's in front, what's behind:**
- **What people see** (the front end): one page — menu on top, custom-order form below, your address and hours at the bottom.
- **Behind the scenes**: nothing yet. The site is just files; WhatsApp carries the order. No database, no server, no monthly bill. (If one day you want to track orders inside the site, that's when a database joins the party.)

**Features I'd suggest** (pick any, or none):
- **Minimum notice** on the custom form: the date picker won't let anyone pick a date sooner than, say, 48 hours. Saves you from "can I have a cake tomorrow?" messages. *(I'd do this first)*
- **"Sold out" / "pause orders" switch** per cake, and one for the whole shop (holidays). You flip it when needed.
- **Opening hours + address block** at the bottom, so people know when they can collect.
- **Allergy / dietary note field** on the custom form (eggless, nut-free, etc.).

Which of these do you want in?

_words: 268 · questions: 1 · files changed: 0 _

## Turn 5

**User:** ooh all of them sound useful honestly. definitely the 48 hour thing and the sold out switch, those feel important. and yeah add the allergy field too, people always ask about nuts.

Great — those three in. I'll also just put your **address and opening hours** as a short text block at the bottom (it's really just typing, not a feature).

Here's how I'd build it, in 4 small steps:

1. **The menu page** — 3 placeholder cakes with photos, prices, "Order on WhatsApp" buttons that open WhatsApp with the order prefilled. Address + hours line at the bottom. ← we start here
2. **Sold-out & pause switches** — a simple flag per cake, plus a shop-wide "closed for orders" banner you can turn on for holidays.
3. **The custom-cake form** — size, flavour, writing on top, pickup date (locked to 48h+ ahead), allergy/dietary note. Submit → prefilled WhatsApp.
4. **Swap placeholders for your real stuff** — your actual cakes, photos, prices, address, hours, WhatsApp number.

Why this way: no database, no monthly bill, no accounts. The site is just files you can drop on any free host (or even email yourself) when it's ready. Each step is something you can open and try.

Worth knowing: your WhatsApp number will be visible in the page's code. That's how WhatsApp links work — anyone looking carefully can find it. For a bakery with a public business number that's normal, but tell me if you'd rather use a separate number just for orders.

Start with step 1?

_words: 223 · questions: 1 · files changed: 0 _

## Turn 6

**User:** yeah go ahead with step 1! and don't worry about the number, it's the same one i already have on my insta so everyone can see it anyway

Building step 1 now. One file, nothing to install — you'll be able to double-click it and see it.

`[tool] Write {"file_path": "<workdir>", "content": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\" />\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n<title>Sweet Crumbs Bakery</title>\n<style>\n  :root {\n    --cream: #fdf6ec;\n    --rose: #e8a9a3;\n    --rose-dark: #c97870;\n    --c`

**Step 1 done: the menu page.**

**Try it:** double-click `index.html` (it's in your project folder). You'll see three placeholder cakes with warm pink/cream colours, prices, and an "Order on WhatsApp" button on each. Click one — WhatsApp (or wa.me in a browser) opens with the order text already written. The number is a placeholder (`+1 000 000 0000`) so it won't actually reach anyone yet; we swap in your real one in step 4.

**The idea:** right now there's no "back end" at all — the page is one file, nothing is saved anywhere. The WhatsApp link is just a special web address (`wa.me/<number>?text=<message>`) that opens WhatsApp with a message pre-written. That's why this works without a database or a server.

Next up is **step 2: the sold-out and "pause orders" switches** — so you can grey out a cake when you run out, or show a "closed for orders" banner when you're on holiday. Ready?

_words: 175 · questions: 1 · files changed: 1 ['index.html']_

## Turn 7

**User:** opened it, looks cute! the pink is nice and the whatsapp button works. yes go ahead with step 2

Yay! Building step 2 now — the sold-out and pause switches.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  .order-btn:hover { background: var(--cocoa); }\n  footer {", "new_string": "  .order-btn:hover { background: var(--cocoa); }\n  .order-btn.disabled {\n    background: #c9c0bc;\n    pointer-events: none;\n    cursor: default;\n  }\n  .cake.sold-out .cake-image`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "</head>\n<body>\n\n<header>", "new_string": "</head>\n<body>\n\n<!-- ============================================================= -->\n<!-- BAKERY SETTINGS \u2014 the only bits you'll normally need to touch -->\n<!-- ===========================================`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  <h2>Today's cakes</h2>\n  <div class=\"menu\">\n\n    <article class=\"cake\">\n      <div class=\"cake-image\">\ud83c\udf6b</div>\n      <div class=\"cake-body\">\n        <div class=\"cake-name\">Chocolate Fudge</div>\n        <div class=\"cake-desc\">Deep `

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  <p>WhatsApp: +1 000 000 0000</p>\n</footer>\n\n</body>", "new_string": "  <p>WhatsApp: +1 000 000 0000</p>\n</footer>\n\n<script>\n  // Shop-wide pause banner\n  if (SHOP_CLOSED) {\n    const banner = document.getElementById('closed-banner');\n    banner.text`

**Step 2 done: sold-out and pause switches.**

**Try it:** reload `index.html`. Nothing looks different yet — that's because both switches are off. Now:
- Open `index.html` in a text editor (TextEdit, VS Code, anything). Near the top you'll see a comment that says `BAKERY SETTINGS` and the line `const SHOP_CLOSED = false;`. Change `false` to `true`, save, reload the page → a dark banner appears up top and every button shows "Orders paused".
- Change it back to `false`. Now find any `<article class="cake" data-sold-out="false">` and change that one to `"true"`, save, reload → that cake goes grey, says "— sold out" next to its name, and its button is disabled.

**The idea:** the page now has **tiny settings** at the top — two switches you flip by changing `false` to `true`. A small bit of JavaScript (code the browser runs when the page loads) looks at those switches and updates how the page looks. No database needed because the "setting" lives in the file itself.

Next up is **step 3: the custom cake form** — size, flavour, writing on top, pickup date (locked to 48h+ ahead), and the allergy note. Submit opens WhatsApp with it all written out. Ready?

_words: 211 · questions: 1 · files changed: 1 ['index.html']_

## Turn 8

**User:** ok that worked, the banner showed up and the one cake went grey. go ahead with step 3

Building step 3 now — the custom cake form.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  #closed-banner {\n    display: none;\n    background: var(--cocoa);\n    color: var(--cream);\n    text-align: center;\n    padding: 14px 20px;\n    font-weight: 500;\n  }\n  footer {", "new_string": "  #closed-banner {\n    display: none;\n    background: va`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "    </article>\n\n  </div>\n</main>", "new_string": "    </article>\n\n  </div>\n\n  <h2>Custom cake order</h2>\n  <p style=\"margin-top:0; opacity:0.8;\">Birthdays, celebrations, something special \u2014 tell us what you'd like and we'll confirm on WhatsApp.</`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  // Flip to true when you're closed for orders (holiday, break, etc.)\n  const SHOP_CLOSED = false;\n  const SHOP_CLOSED_MESSAGE = \"We're closed for orders this week. Back soon!\";", "new_string": "  // Your WhatsApp number in international format, digits onl`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "<script>\n  // Shop-wide pause banner\n  if (SHOP_CLOSED) {\n    const banner = document.getElementById('closed-banner');\n    banner.textContent = SHOP_CLOSED_MESSAGE;\n    banner.style.display = 'block';\n  }\n\n  // Sold-out and pause handling per cake\n  do`

**Step 3 done: the custom cake form.**

**Try it:** reload `index.html`. Below the menu you'll see a new "Custom cake order" section with fields: name, size, flavour, writing on top, pickup date, allergy note, and extra notes.
- Try picking a pickup date — it won't let you pick anything within the next 48 hours.
- Fill in a few fields and hit "Send order on WhatsApp" → WhatsApp opens with a tidy multi-line message with everything you entered.
- Flip `SHOP_CLOSED` to `true` and reload → the custom-form submit button also goes grey and says "Orders paused", same as the menu buttons.

**The idea:** when you hit submit, a bit of JavaScript collects all the field values, stitches them into a readable message, and opens a WhatsApp link with that message prefilled. The 48-hour minimum is set on the date picker when the page loads — it's a soft lock (someone technical could bypass it in their browser), but good enough for a trust-based WhatsApp flow.

Last up is **step 4: swap the placeholder cakes, prices, photos, address and WhatsApp number for your real stuff.** For this, I'll need a few things from you — can you tell me:
- Your bakery's real **name**?

_words: 214 · questions: 1 · files changed: 1 ['index.html']_

## Metrics

| Turn | Words | Questions | Files changed | Proposal |
|---|---|---|---|---|
| 1 | 231 | 1 | 0 |  |
| 2 | 151 | 1 | 0 |  |
| 3 | 105 | 1 | 0 |  |
| 4 | 268 | 1 | 0 | yes |
| 5 | 223 | 1 | 0 |  |
| 6 | 175 | 1 | 1 |  |
| 7 | 211 | 1 | 1 |  |
| 8 | 214 | 1 | 1 |  |

- Turns: 8
- First file change on turn: 6
- Most files changed in one turn: 1
- Proposal (how it works, front/back, suggested features) on turn: 4 (before first code change)
- Turns asking more than one question: 0
- Turns ending with no question: 0
- Average words per turn: 197
