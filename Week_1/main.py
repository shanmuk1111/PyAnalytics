import csv
from pathlib import Path


DATA_FILE = Path(__file__).parent / "data" / "expenses.csv"


def load_expenses(path):
    """Read expenses from a CSV file and return a list of dictionaries."""
    expenses = []

    with open(path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        required_columns = {"date", "category", "description", "amount"}
        if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
            raise ValueError(
                "CSV must contain these columns: date, category, description, amount"
            )

        for row in reader:
            row["category"] = row["category"].strip().title()
            row["description"] = row["description"].strip()
            row["amount"] = float(row["amount"])
            expenses.append(row)

    return expenses


def total_spent(expenses):
    """Return the sum of all expense amounts."""
    return sum(expense["amount"] for expense in expenses)


def totals_by_category(expenses):
    """Return a dictionary containing the total amount for each category."""
    totals = {}

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]
        totals[category] = totals.get(category, 0.0) + amount

    return totals


def biggest_expense(expenses):
    """Return the expense row with the largest amount."""
    if not expenses:
        return None

    return max(expenses, key=lambda expense: expense["amount"])


def display_expenses(expenses):
    """Display all expenses in aligned columns."""
    print("\nALL EXPENSES")
    print("-" * seventy)
    print(f"{'DATE':<12} {'CATEGORY':<14} {'DESCRIPTION':<24} {'AMOUNT (INR)':>14}")
    print("-" * seventy)

    for expense in expenses:
        print(
            f"{expense['date']:<12} "
            f"{expense['category']:<14} "
            f"{expense['description']:<24} "
            f"{expense['amount']:>14.2f}"
        )

    print("-" * seventy)
    print(f"{'TOTAL':<52} {total_spent(expenses):>14.2f}")


def display_category_totals(expenses):
    """Display total spending for each category."""
    print("\nTOTALS BY CATEGORY")
    print("-" * thirty)
    print(f"{'CATEGORY':<16} {'AMOUNT (INR)':>14}")
    print("-" * thirty)

    for category, amount in sorted(totals_by_category(expenses).items()):
        print(f"{category:<16} {amount:>14.2f}")

    print("-" * thirty)
    print(f"{'OVERALL TOTAL':<16} {total_spent(expenses):>14.2f}")


def display_biggest_expense(expenses):
    """Display the single largest expense."""
    expense = biggest_expense(expenses)

    if expense is None:
        print("\nNo expenses found.")
        return

    print("\nBIGGEST EXPENSE")
    print("-" * thirty)
    print(f"Date        : {expense['date']}")
    print(f"Category    : {expense['category']}")
    print(f"Description : {expense['description']}")
    print(f"Amount      : INR {expense['amount']:.2f}")


def main():
    """Run the menu-driven expense tracker."""
    try:
        expenses = load_expenses(DATA_FILE)
    except FileNotFoundError:
        print(f"Error: CSV file not found: {DATA_FILE}")
        return
    except (ValueError, csv.Error) as error:
        print(f"Error while reading CSV: {error}")
        return

    while True:
        print("\n========== PYANALYTICS EXPENSE TRACKER ==========")
        print("1. Show all expenses")
        print("2. Show totals by category")
        print("3. Show biggest expense")
        print("4. Quit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            display_expenses(expenses)
        elif choice == "2":
            display_category_totals(expenses)
        elif choice == "3":
            display_biggest_expense(expenses)
        elif choice == "4":
            print("Thank you for using PyAnalytics. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")


seventy = 70
thirty = 30

if __name__ == "__main__":
    main()
