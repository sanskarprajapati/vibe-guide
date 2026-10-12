## Turn 1

Using your profile: public waitlist that stores strangers' emails, tier T2.
Type /vibe at the start of each session to keep this mode on.

Right now your signup form works, but the email only gets printed to the server log and then disappears. You need somewhere permanent to keep the emails. For a public page on a budget under $20 a month, here's what fits:

1. **Supabase** (a hosted database plus a login system your app can talk to), recommended
   Fits you because: your profile says you'll store logins later too, and Supabase covers the database and logins in one place. Underneath it's a standard database, so you can move your data out later.
   Cost at your size: free tier is plenty for a waitlist. Paid plans are flat monthly, not per click. Check current pricing before you grow past the free tier.
   Watch out for: you have to set up its access rules correctly, or strangers could read your list. I'll set those up for you and show you where to check them.

2. **Neon** (a hosted database only, no login system or built-in access rules)
   Fits you because: very simple if all you ever want is a list of emails. Same standard database type, easy to leave.
   Cost at your size: free tier covers a waitlist.
   Watch out for: when you add logins, you'll need a second service for that, so more pieces to manage.

3. **Firebase** (Google's database and login service, charges per read and write): not a fit for you, because pay-per-use pricing is less predictable on a small fixed budget, and its data format is Firebase-specific, which makes switching later harder.

Which one?
