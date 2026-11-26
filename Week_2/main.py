"""Menu interface for the PyAnalytics expense tracker."""

from datetime import datetime
from pathlib import Path

from tracker import Expense, ExpenseTracker
from storage import load_expenses, append_expense, export_report_json

PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "data" / "expenses.csv"
REPORT_FILE = PROJECT_DIR / "report.json"


def show_all_expenses(tracker):
    print("\nALL EXPENSES")
    print("-" * 76)
    print(f"{'DATE':<12} {'CATEGORY':<14} {'DESCRIPTION':<25} {'AMOUNT (INR)':>14}")
    print("-" * 76)
    for expense in tracker.expenses:
        print(expense)
    print("-" * 76)
    print(f"{'TOTAL':<51} {tracker.total_spent():>14.2f}")
    print(f"Valid records: {len(tracker.expenses)}")


def show_category_totals(tracker):
    print("\nTOTALS BY CATEGORY")
    print("-" * 34)
    print(f"{'CATEGORY':<18} {'AMOUNT (INR)':>14}")
    print("-" * 34)
    for category, amount in sorted(tracker.totals_by_category().items()):
        print(f"{category:<18} {amount:>14.2f}")
    print("-" * 34)
    print(f"{'OVERALL TOTAL':<18} {tracker.total_spent():>14.2f}")


def show_biggest_expense(tracker):
    expense = tracker.biggest_expense()
    if expense is None:
        print("\nNo expenses found.")
        return
    print("\nBIGGEST EXPENSE")
    print("-" * 35)
    print(f"Date        : {expense.date}")
    print(f"Category    : {expense.category}")
    print(f"Description : {expense.description}")
    print(f"Amount      : INR {expense.amount:.2f}")


def add_new_expense(tracker):
    print("\nADD NEW EXPENSE")
    date = input("Date (YYYY-MM-DD): ").strip()
    category = input("Category: ").strip()
    description = input("Description: ").strip()
    amount_text = input("Amount (INR): ").strip()

    if not date or not category or not description:
        print("Date, category and description cannot be blank.")
        return

    try:
        amount = float(amount_text)
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Invalid amount. Enter a number, for example 125 or 125.50.")
        return

    expense = Expense(date, category, description, amount)
    append_expense(DATA_FILE, expense)
    tracker.add_expense(expense)
    print("Expense added and saved to data/expenses.csv.")


def search_expenses(tracker):
    keyword = input("\nEnter a description keyword: ").strip()
    matches = tracker.search(keyword)
    if not matches:
        print("No matching expenses found.")
        return

    print(f"\nSEARCH RESULTS ({len(matches)} found)")
    print("-" * 76)
    print(f"{'DATE':<12} {'CATEGORY':<14} {'DESCRIPTION':<25} {'AMOUNT (INR)':>14}")
    print("-" * 76)
    for expense in matches:
        print(expense)


def export_report(tracker):
    report = export_report_json(REPORT_FILE, tracker)
    print(f"\nReport exported to: {REPORT_FILE.name}")
    print(f"Overall total: INR {report['overall_total']:.2f}")
    print(f"Categories exported: {len(report['category_totals'])}")


def main():
    try:
        expenses, skipped_rows = load_expenses(DATA_FILE)
    except (FileNotFoundError, OSError, ValueError) as error:
        print(f"Could not load expense data: {error}")
        return

    tracker = ExpenseTracker(expenses)
    print("PyAnalytics loaded successfully.")
    print(f"Valid expense rows: {len(expenses)}")
    print(f"Skipped invalid/blank rows: {skipped_rows}")

    while True:
        print("\n========== PYANALYTICS EXPENSE TRACKER ==========")
        print("1. Show all expenses")
        print("2. Show totals by category")
        print("3. Show biggest expense")
        print("4. Add expense")
        print("5. Search by description")
        print("6. Export report (JSON)")
        print("7. Quit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            show_all_expenses(tracker)
        elif choice == "2":
            show_category_totals(tracker)
        elif choice == "3":
            show_biggest_expense(tracker)
        elif choice == "4":
            add_new_expense(tracker)
        elif choice == "5":
            search_expenses(tracker)
        elif choice == "6":
            export_report(tracker)
        elif choice == "7":
            print("Thank you for using PyAnalytics. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
