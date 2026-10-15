# bakery-orders (skill)

**Persona:** You run a small home bakery and sell cakes to locals through Instagram DMs today. You've never built a website. You want people to see your cakes and order ahead for pickup. You'd like to take payment if it's not complicated, but you're worried about fees and doing something wrong with card details. Answer in short casual messages.

## Turn 1

**User:** /vibe i want a simple website for my bakery where people can see the menu and order cakes

`[tool] Bash {"command": "ls -la <workdir> 2>/dev/null && echo \"---\" && ls -la <workdir> 2>/dev/null", "description": "List project directory and check for .vibe folder"}`

`[tool] Read {"file_path": "<workdir>"}`

A bakery site with a menu and cake orders — nice project. Before I plan anything, there's one big question that changes almost everything about how we build it.

**What happens when someone orders a cake?** This decides whether we need a payment system (big setup) or a simple form (quick to build).

`[tool] AskUserQuestion {"questions": [{"question": "What happens when someone orders a cake on the site?", "header": "Order flow", "multiSelect": false, "options": [{"label": "Request form \u2014 you contact them", "description": "They pick a cake, leave their details, and you get the order by email or message. Payment happens later (in person, bank transfer, etc.). Simplest to build, nothing to set up with banks. Good `

A bakery site with a menu and cake orders — nice. Before I plan anything, there's one big question that shapes everything else.

**What happens when someone orders a cake on the site?** This decides whether we need an online payment setup (bigger project) or just a simple form (quick to build).

a. **Request form, you contact them.** They pick a cake, leave their details, and the order lands in your email. They pay you later — in person, bank transfer, whatever suits. Simplest to build, nothing to set up with banks. *(my pick for a small bakery starting out)*

b. **Pay online with card.** Real checkout on the site, money lands in your account automatically. Needs a payment service like **Stripe** (a company that handles card payments for small businesses — takes a small fee per order). More setup, and you'd also need to handle refunds.

c. **Reserve now, pay at pickup.** They choose a cake and reserve it; they pay in cash or card when they collect. No online payments, but it still feels like a "proper" order.

Which fits what you had in mind?

_words: 240 · questions: 1 · files changed: 0 _

## Turn 2

**User:** honestly a sounds easiest for now, i don't wanna mess with card stuff yet. maybe we add payments later if it gets busy?

Easy wins first — smart. We can add payments later when it's worth the extra setup.

Next shaping question: **how do your cakes work on the menu?** This changes what the ordering page looks like.

a. **Set menu with fixed prices.** You list, say, 6–10 cakes (chocolate £25, red velvet £30, etc.). People pick one, maybe choose a size, done. Clear and fast. *(my pick for simple)*

b. **Custom cakes only.** No fixed list — people describe their dream cake (occasion, flavour, colours, how many people), and you reply with a quote. More personal, but more back-and-forth email per order.

c. **Both — menu plus a "custom cake" option.** A list of your signature cakes, and one extra button for "something custom" that sends an inquiry. Nice middle ground, bit more to build.

Which matches how you actually sell cakes today?

_words: 141 · questions: 1 · files changed: 0 _

## Turn 3

**User:** honestly it's mostly c for me - i have my regulars like chocolate fudge and lemon drizzle but tons of people want custom for birthdays and stuff. let's do both

Nice — signature cakes with a custom option is a very "real bakery" feel.

Next thing: **do customers pick up from you, or do you deliver too?** This changes what we ask on the order form.

a. **Pickup only.** They come to collect from your shop. No address needed, no delivery fee to work out. Simplest form. *(my pick for a first version)*

b. **Delivery only, in your local area.** You'd deliver every order. The form needs their address and we'd need to decide a delivery fee or area limit.

c. **Both — customer chooses pickup or delivery.** Nice flexibility, but the form has to show/hide the address bit depending on what they pick, and you'll need delivery rules.

Which one matches how you work now?

_words: 126 · questions: 1 · files changed: 0 _

## Turn 4

**User:** pickup only for now, that's how I do it with insta orders anyway

Perfect — matches your current flow nicely.

Last big question, then I'll sketch the plan: **where should the order actually land when someone submits it?**

a. **Email to you.** The form sends you an email with all the details (cake, size, pickup date, their phone, notes). You reply or call them back. Needs a tiny free service called **Formspree** (an inbox-forwarder for website forms — no code needed, free up to 50 orders/month). *(my pick — reliable and keeps a record)*

b. **WhatsApp message to you.** The "Place order" button opens the customer's WhatsApp with their order details pre-filled, and they hit send to you. Zero setup, instant on your phone, and since you already do insta orders this feels familiar. Downside: no automatic record if they don't send it, and no backup inbox.

c. **Both — email and a WhatsApp button.** Customer picks whichever is easier for them. A bit more to design but covers everyone.

Which feels right for you?

_words: 162 · questions: 1 · files changed: 0 _

## Turn 5

**User:** b sounds easiest, whatsapp is already on my phone and i check it all day. let's go with that

Great — WhatsApp is spot on for a bakery like yours. I've got enough to plan.

Here's how I'd build it, in 4 small steps:
1. **The site itself** — a one-page site with a Welcome, Menu, Order form, and a WhatsApp "Send order" button. Placeholder cakes to start. ← we start here
2. **Your real menu** — swap in your signature cakes with photos, prices and descriptions.
3. **Make it look like your brand** — colours, fonts, a nice hero image, and check it looks good on phones.
4. **Put it online** — a free host so you can share the link on Instagram.

Why this way: no accounts, no database, no payments — just a page that opens WhatsApp with the order filled in. Costs £0 to run, and you can take it live in a day.

Worth knowing: anyone can see your WhatsApp number if they view the page (same as having it in your Insta bio — fine for a business number, not for a personal one). Confirm the number we use is the one you share publicly.

Start with step 1?

_words: 186 · questions: 1 · files changed: 0 _

## Turn 6

**User:** Yep that number's my business one, I share it on Insta anyway. Go for it, start step 1!

Building the skeleton now.

`[tool] Write {"file_path": "<workdir>", "content": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n  <title>Sweet Crumb Bakery \u2014 Fresh Cakes</title>\n  <link rel=\"stylesheet\" href=\"styles.css\">\n</head>\n<body>\n\n  <header c`

`[tool] Write {"file_path": "<workdir>", "content": "* { box-sizing: border-box; margin: 0; padding: 0; }\n\nbody {\n  font-family: Georgia, 'Times New Roman', serif;\n  background: #fdf7ef;\n  color: #3d2b1f;\n  line-height: 1.6;\n}\n\n.hero {\n  text-align: center;\n  padding: 4rem 1.5rem 3rem;\n  background: linear-gradient(180deg, #f`

**Step 1 done: the skeleton site.**

**Try it:** open `index.html` by double-clicking it (or dragging it into a browser tab). You'll see a bakery page with 4 placeholder cakes, an order form, and a brown "Send order via WhatsApp" button. Fill it in and hit send — a WhatsApp window will pop up with the order already typed out, ready to send. (It'll go to a fake number for now; we'll fix that in step 2.)

**The idea:** this is a **static site** (just an HTML file + a CSS file sitting on your computer — no server, no database, no login). The clever bit is the Send button: it builds a WhatsApp link like `wa.me/<your-number>?text=<order-details>`, so clicking it opens WhatsApp with the message pre-filled. That's why we don't need any backend — WhatsApp handles the "sending" part.

**Placeholders I used** (we'll swap all of these next): bakery name "Sweet Crumb Bakery", three generic cakes with made-up prices, and a fake WhatsApp number.

**Next is step 2: your real menu.** To do that I'll need from you:
- The actual name of your bakery
- Your WhatsApp business number (I'll format it right)
- 3–5 of your signature cakes — for each one: name, short description (1 line), and a starting price

Want to send those over now?

_words: 222 · questions: 1 · files changed: 2 ['index.html', 'styles.css']_

## Turn 7

**User:** yeah ok i opened it and it looks like you said, little brown button and everything. bakery name is Luna's Little Cakes, my whatsapp is 415-555-0132. for cakes: 1) Classic Vanilla Bean - fluffy vanilla with buttercream, $35. 2) Chocolate Fudge - rich dark chocolate with ganache, $40. 3) Strawberry Shortcake - fresh berries and whipped cream, $42. 4) Lemon Lavender - light and floral, $38.

Love "Luna's Little Cakes" — making the swap now.

Quick heads-up on the number: `415-555-0132` is a reserved **fake number** in the US (anything in 555-0100 to 555-0199 is set aside for fiction/examples, so real customers tapping Send won't reach you). I'll put it in so you can see everything working, but we'll need your real WhatsApp business number before step 4 when we put the site online.

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  <title>Sweet Crumb Bakery \u2014 Fresh Cakes</title>", "new_string": "  <title>Luna's Little Cakes \u2014 Handmade Cakes</title>"}`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "    <h1>Sweet Crumb Bakery</h1>", "new_string": "    <h1>Luna's Little Cakes</h1>"}`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "      <article class=\"cake-card\">\n        <div class=\"cake-photo cake-photo-1\"></div>\n        <h3>Chocolate Fudge</h3>\n        <p class=\"cake-desc\">Rich, moist, with a glossy fudge icing.</p>\n        <p class=\"cake-price\">from \u00a325</p>\n      </`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "          <option value=\"\">\u2014 choose one \u2014</option>\n          <option>Chocolate Fudge</option>\n          <option>Lemon Drizzle</option>\n          <option>Vanilla Celebration</option>\n          <option>Custom cake (I'll describe below)</option>", `

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "    // Your WhatsApp number in international format: country code + number, no spaces, no \"+\".\n    // Example: UK 07123 456 789 becomes 447123456789.\n    const WHATSAPP_NUMBER = \"447123456789\"; // placeholder \u2014 we'll replace this with yours", "new_st`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "    <p>Sweet Crumb Bakery \u00b7 Pickup only \u00b7 Handmade to order</p>", "new_string": "    <p>Luna's Little Cakes \u00b7 Pickup only \u00b7 Handmade to order</p>"}`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": ".cake-photo-1 { background: #4a2c1f; }\n.cake-photo-2 { background: #f4e07a; }\n.cake-photo-3 { background: #faf0e6; }\n.cake-photo-custom { background: #e8d5c4; }", "new_string": ".cake-photo-1 { background: #f5e6c8; }\n.cake-photo-2 { background: #4a2c1f; }\n`

**Step 2 done: your real menu is in.**

**Try it:** refresh the page in your browser. You'll see "Luna's Little Cakes" at the top, your 4 cakes with prices in $, and the custom cake card. The order dropdown now has all your cakes. Fill it in and submit — WhatsApp will open with your actual menu in the order details (still going to the fake number for now).

**The idea:** websites keep **structure** (the layout and form from step 1) separate from **content** (the words and prices you just gave me). That's why swapping cakes in only touched the parts that needed changing — the form, buttons, and layout stayed the same.

**Small thing I did:** each cake card has a coloured tile instead of a photo for now — cream for vanilla, dark brown for chocolate, pink for strawberry, lavender for lemon lavender. In step 3 we can replace these with real photos if you have them.

**Next is step 3: make it feel like Luna's.** The name "Luna" has a nice dreamy, moonlit feel — but you tell me. Which vibe fits what you have in mind?

a. **Dreamy pastels** — soft pinks, lavender, cream, maybe a hand-written-style title font. Feminine and romantic, leans into the "Luna" name. *(my pick based on the name)*

b. **Warm and homey** — creams, browns, cosy serif fonts, like now but tightened up. Comfortable, "neighbourhood bakery" feel.

c. **Clean and modern** — mostly white with one accent colour (say dusty rose or sage green), simple sans-serif font. More upscale/boutique.

Which direction?

_words: 328 · questions: 2 · files changed: 2 ['index.html', 'styles.css']_

## Turn 8

**User:** oh good catch on the number, i'll grab my real one before we go live. and yeah option a sounds perfect, dreamy pastels fits luna 💕

Lovely — leaning into the Luna vibe now.

`[tool] Read {"file_path": "<workdir>"}`

`[tool] Write {"file_path": "<workdir>", "content": "* { box-sizing: border-box; margin: 0; padding: 0; }\n\nbody {\n  font-family: 'Quicksand', 'Avenir', 'Helvetica Neue', sans-serif;\n  background: #fdf5f9;\n  color: #4a3647;\n  line-height: 1.6;\n}\n\n.hero {\n  text-align: center;\n  padding: 4.5rem 1.5rem 3.5rem;\n  background: line`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "  <title>Luna's Little Cakes \u2014 Handmade Cakes</title>\n  <link rel=\"stylesheet\" href=\"styles.css\">", "new_string": "  <title>Luna's Little Cakes \u2014 Handmade Cakes</title>\n  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n  <link r`

`[tool] Edit {"replace_all": false, "file_path": "<workdir>", "old_string": "    <h1>Luna's Little Cakes</h1>\n    <p class=\"tagline\">Handmade cakes, baked fresh for your special day</p>", "new_string": "    <h1>Luna's Little Cakes</h1>\n    <div class=\"moon-motif\" aria-hidden=\"true\">\u263e \u00b7 \u2726 \u00b7 \u263e</div>\n    <`

**Step 3 done: the Luna's vibe is in.**

**Try it:** refresh the browser. You should see a soft pink-and-lavender gradient at the top, "Luna's Little Cakes" in flowing handwritten script, a tiny moon motif beneath it, cake cards that gently lift when you hover, and a pink gradient order button. The form sits in its own white rounded card. All in dreamy pastels.

**The idea:** this used **web fonts** (fonts loaded from Google's servers, so every visitor sees the same handwritten "Dancing Script" lettering — not just people who happen to have that font installed on their computer). The two little `<link>` tags at the top of the HTML pull them in.

**One decision before we go online.** Right now each cake card has a soft pastel coloured tile instead of a real photo. For a bakery, photos really sell orders. What would you like?

a. **Real photos.** You send me 4 cake photos (just copy from your Instagram and drop them in a folder), and I'll place one on each card. Big visual upgrade, but you need the photos ready. *(my pick — nothing sells cake like a cake photo)*

b. **Keep the pastel tiles.** Simplest, keeps the dreamy minimal look, no photo-prep needed. We can add photos later.

c. **Real photos for the 4 cakes, keep the ✦ star tile for custom cakes.** Best of both — real cake visuals where they count, no need to invent a "custom cake" photo.

Which way?

_words: 253 · questions: 2 · files changed: 2 ['index.html', 'styles.css']_

## Metrics

| Turn | Words | Questions | Files changed |
|---|---|---|---|
| 1 | 240 | 1 | 0 |
| 2 | 141 | 1 | 0 |
| 3 | 126 | 1 | 0 |
| 4 | 162 | 1 | 0 |
| 5 | 186 | 1 | 0 |
| 6 | 222 | 1 | 2 |
| 7 | 328 | 2 | 2 |
| 8 | 253 | 2 | 2 |

- Turns: 8
- First file change on turn: 6
- Most files changed in one turn: 2
- Turns asking more than one question: 2
- Turns ending with no question: 0
- Average words per turn: 207
