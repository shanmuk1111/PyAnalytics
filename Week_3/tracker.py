
from db import add_expense, get_all, totals_by_category


class ExpenseTracker:

    def __init__(self, conn):
        self.conn = conn

    def add_expense(self, date, category, description, amount):
        return add_expense(
            self.conn,
            date,
            category,
            description,
            amount
        )

    def get_all(self, month=None):
        return get_all(self.conn, month)

    def totals_by_category(self, month=None):
        return totals_by_category(self.conn, month)
