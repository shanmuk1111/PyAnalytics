"""CSV and JSON file operations for PyAnalytics."""

import csv
import json
from pathlib import Path

from tracker import Expense

FIELDNAMES = ["date", "category", "description", "amount"]


def load_expenses(path):
    """
    Load valid CSV rows as Expense objects.

    Returns (expenses, skipped_rows). Blank rows, missing fields and
    non-numeric amounts are skipped instead of stopping the program.
    """
    expenses = []
    skipped_rows = 0
    path = Path(path)

    with path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV file is empty or has no header.")

        # Normalise header whitespace and verify the required columns.
        reader.fieldnames = [name.strip() if name else "" for name in reader.fieldnames]
        missing = set(FIELDNAMES) - set(reader.fieldnames)
        if missing:
            raise ValueError(
                "CSV is missing required column(s): " + ", ".join(sorted(missing))
            )

        for row in reader:
            if not row or all(value is None or not str(value).strip() for value in row.values()):
                skipped_rows += 1
                continue

            date = (row.get("date") or "").strip()
            category = (row.get("category") or "").strip().title()
            description = (row.get("description") or "").strip()
            amount_text = (row.get("amount") or "").strip()

            if not date or not category or not description or not amount_text:
                skipped_rows += 1
                continue

            try:
                amount = float(amount_text)
            except (TypeError, ValueError):
                skipped_rows += 1
                continue

            if amount < 0:
                skipped_rows += 1
                continue

            expenses.append(Expense(date, category, description, amount))

    return expenses, skipped_rows


def append_expense(path, expense):
    """Append one Expense object to the CSV file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = path.exists() and path.stat().st_size > 0

    with path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "date": expense.date,
            "category": expense.category,
            "description": expense.description,
            "amount": f"{expense.amount:.2f}",
        })


def export_report_json(path, tracker):
    """Write category totals and overall total to a JSON report."""
    report = {
        "currency": "INR",
        "expense_count": len(tracker.expenses),
        "overall_total": round(tracker.total_spent(), 2),
        "category_totals": {
            category: round(amount, 2)
            for category, amount in sorted(tracker.totals_by_category().items())
        },
    }

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)
    return report
