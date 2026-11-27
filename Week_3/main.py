
import argparse
import sqlite3
import sys
from datetime import date, datetime

from db import get_connection, add_expense, get_all, totals_by_category, delete_expense
from storage import import_csv
from tracker import ExpenseTracker


def valid_month(month):
    try:
        datetime.strptime(month, "%Y-%m")
        return month
    except ValueError:
        raise ValueError("Month must use YYYY-MM format, e.g. 2025-03")


def show_summary(tracker, month=None):

    expenses = tracker.get_all(month)
    totals = tracker.totals_by_category(month)

    print("\n========== EXPENSE SUMMARY ==========")

    if month:
        print("Month:", month)

    if not expenses:
        print("No expenses found.")
        return

    for row in totals:
        print(f"{row['category']}: INR {row['total']:.2f}")

    total = sum(row["amount"] for row in expenses)

    print("-------------------------------------")
    print(f"Total: INR {total:.2f}")
    print(f"Number of expenses: {len(expenses)}")


def main():

    parser = argparse.ArgumentParser(
        description="PyAnalytics Expense Tracker"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # Import command
    import_parser = subparsers.add_parser(
        "import",
        help="Import expenses from CSV"
    )
    import_parser.add_argument("path")

    # Summary command
    summary_parser = subparsers.add_parser(
        "summary",
        help="Show expense summary"
    )
    summary_parser.add_argument("--month")

    # Add command
    add_parser = subparsers.add_parser(
        "add",
        help="Add a new expense"
    )
    add_parser.add_argument("--date", default=date.today().isoformat())
    add_parser.add_argument("--category")
    add_parser.add_argument("--description")
    add_parser.add_argument("--amount", type=float)

    # Delete command (optional stretch goal)
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete an expense using its ID"
    )
    delete_parser.add_argument("id", type=int)

    args = parser.parse_args()

    conn = None

    try:
        conn = get_connection()
        tracker = ExpenseTracker(conn)

        if args.command == "import":

            imported, skipped, invalid = import_csv(
                args.path,
                conn
            )

            print("\nImport completed.")
            print("Imported:", imported)
            print("Duplicates skipped:", skipped)
            print("Invalid rows skipped:", invalid)

        elif args.command == "summary":

            if args.month:
                valid_month(args.month)

            show_summary(tracker, args.month)

        elif args.command == "add":

            category = args.category or input("Category: ")
            description = args.description or input("Description: ")

            if args.amount is None:
                amount = float(input("Amount: "))
            else:
                amount = args.amount

            if amount < 0:
                raise ValueError("Amount cannot be negative.")

            datetime.strptime(args.date, "%Y-%m-%d")

            tracker.add_expense(
                args.date,
                category,
                description,
                amount
            )

            print("Expense added successfully.")

        elif args.command == "delete":

            if delete_expense(conn, args.id):
                print("Expense deleted successfully.")
            else:
                print("Expense ID not found.")

    except (FileNotFoundError, ValueError, OSError, sqlite3.Error) as error:

        print(f"Error: {error}", file=sys.stderr)
        return 1

    finally:
        if conn:
            conn.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
