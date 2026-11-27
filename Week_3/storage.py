
import csv
from pathlib import Path
from datetime import datetime

from db import add_expense


def import_csv(path, conn):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    required_columns = {
        "date",
        "category",
        "description",
        "amount"
    }

    imported = 0
    skipped = 0
    invalid = 0

    with open(path, "r", newline="", encoding="utf-8-sig") as file:

        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV file is empty or has no header.")

        headers = {
            name.strip().lower(): name
            for name in reader.fieldnames if name
        }

        missing = required_columns - set(headers)

        if missing:
            raise ValueError(
                "Wrong CSV columns. Missing: " + ", ".join(sorted(missing))
            )

        for line_number, row in enumerate(reader, start=2):

            try:
                date = row[headers["date"]].strip()
                category = row[headers["category"]].strip()
                description = row[headers["description"]].strip()
                amount = float(row[headers["amount"]].strip())

                datetime.strptime(date, "%Y-%m-%d")

                if not date or not category or not description:
                    raise ValueError("Missing required data")

                if amount < 0:
                    raise ValueError("Negative amount")

                source_key = f"{path.resolve()}:{line_number}"

                success = add_expense(
                    conn,
                    date,
                    category,
                    description,
                    amount,
                    source_key
                )

                if success:
                    imported += 1
                else:
                    skipped += 1

            except (ValueError, TypeError, AttributeError):
                print(f"Skipped invalid row at line {line_number}")
                invalid += 1

    return imported, skipped, invalid
