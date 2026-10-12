## Turn 1

Using your profile: a script only you run on your own computer, tier T0.

Type /vibe at the start of each session to keep this mode on.

I'm saving the results to a new file on your computer, `contacts_cleaned.csv`, in the same folder as your other files. It's a CSV (a plain text file laid out like a spreadsheet, opens in Excel or Google Sheets), the same kind of file you started with. There's no need for a database or an online service here: you're the only one using it, and the file stays on your laptop.

I ran it on your contacts and it worked:

```
name,email,city
Asha,asha@example.com,Pune
Meera,meera@example.com,Jaipur
```

Ravi was left out because his row has no email. That's how the cleaner was already set up.

What changed:
- `clean.py` now saves the cleaned contacts to `contacts_cleaned.csv` instead of only showing them on screen. Your original `contacts.csv` stays as it was.
- Each run replaces the old cleaned file with a fresh one, so if you want to keep an older copy, rename it first.
- To look at the results, double-click `contacts_cleaned.csv` or open it in Excel or Google Sheets. To refresh it, run `python clean.py contacts.csv` again.
