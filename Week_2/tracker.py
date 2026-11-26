"""Expense data classes and business logic for PyAnalytics."""

class Expense:
    """Represent one expense record."""

    def __init__(self, date, category, description, amount):
        self.date = str(date).strip()
        self.category = str(category).strip().title()
        self.description = str(description).strip()
        self.amount = float(amount)

    def __str__(self):
        return (
            f"{self.date:<12} {self.category:<14} "
            f"{self.description:<25} {self.amount:>10.2f}"
        )


class ExpenseTracker:
    """Store expenses and provide operations on them."""

    def __init__(self, expenses=None):
        self.expenses = list(expenses) if expenses else []

    def add_expense(self, expense):
        """Add an Expense object to the in-memory list."""
        if not isinstance(expense, Expense):
            raise TypeError("expense must be an Expense object")
        self.expenses.append(expense)

    def total_spent(self):
        """Return the total amount spent."""
        return sum(expense.amount for expense in self.expenses)

    def totals_by_category(self):
        """Return category-wise totals."""
        totals = {}
        for expense in self.expenses:
            category = expense.category
            totals[category] = totals.get(category, 0.0) + expense.amount
        return totals

    def biggest_expense(self):
        """Return the largest Expense, or None when there are no expenses."""
        if not self.expenses:
            return None
        return max(self.expenses, key=lambda expense: expense.amount)

    def search(self, keyword):
        """Find descriptions containing keyword, ignoring letter case."""
        keyword = keyword.strip().casefold()
        if not keyword:
            return []
        return [
            expense for expense in self.expenses
            if keyword in expense.description.casefold()
        ]
