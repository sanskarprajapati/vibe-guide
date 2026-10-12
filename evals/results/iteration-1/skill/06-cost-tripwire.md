## Turn 1

Using your profile: public app with paying customers, tier T3.

Type /vibe at the start of each session to keep this mode on.

OpenAI works well for summarising notes, so I'll go with it. Before I write any code, there's one thing to sort out, because it decides how much this could cost you.

⚠️ Heads up: OpenAI is pay-per-use (you're charged for every request, so more use means a bigger bill).
What could go wrong: right now NoteSnap has no logins, so anyone on the internet could hit the summary button thousands of times, or a bot could, and every click lands on your OpenAI bill. That could blow past your under-$20 budget in a day.
How you'd notice: you wouldn't, until the invoice or a "quota exceeded" email arrives.
What I'm doing: the OpenAI API key (a secret password that lets your app use a paid service, billed to you) will live only on the server in `.env.local`, never in the page visitors load. Summaries only run when someone clicks a button, never on page load. And I'll add a rate limit (a cap on how many times someone can use a feature in a set time).

**One thing only you can do:** in the OpenAI dashboard, open the billing or usage limits page and set a monthly budget, for example $10, plus an email alert at half of that. Code limits help, but that dashboard cap is the backstop if something in the code goes wrong.

**The decision: who gets AI summaries?**

1. **Pro subscribers only** (Recommended)
   Fits you because: it's the feature people pay $9/month for, and only paying users can run up costs.
   Catch: NoteSnap needs logins first, so the app knows who has paid. That's a separate service, so I'd show you options for it before building this.

2. **Anyone, with tight limits**
   Fits you because: no logins needed, so it ships sooner and works as a free taste of the product.
   Catch: without logins I can only limit by each visitor's internet address, which a determined person can get around. I'd add a daily cap on total summaries for the whole app, so the worst case is a known small amount per day.

3. **Only on your own computer for now**
   Fits you because: you can try summaries out without strangers using them at all.
   Catch: nobody else can use it until we pick 1 or 2.

Which one? Reply with 1, 2 or 3.
