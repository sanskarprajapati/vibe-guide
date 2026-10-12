import csv
import sys


def clean_rows(rows):
    """Trim whitespace and drop rows with no email."""
    cleaned = []
    for row in rows:
        trimmed = {k.strip(): (v or "").strip() for k, v in row.items()}
        if trimmed.get("email"):
            cleaned.append(trimmed)
    return cleaned


def main(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    for row in clean_rows(rows):
        print(row)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "contacts.csv")
