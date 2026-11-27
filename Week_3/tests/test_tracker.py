
import unittest
import tempfile
from pathlib import Path

from db import get_connection, add_expense, get_all, totals_by_category
from tracker import ExpenseTracker
from storage import import_csv


class TestExpenseTracker(unittest.TestCase):


    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()

        self.db_path = Path(self.temp.name) / "test.db"

        self.conn = get_connection(self.db_path)

        self.tracker = ExpenseTracker(self.conn)


    def tearDown(self):
        self.conn.close()
        self.temp.cleanup()

    def test_add_expense(self):
        self.tracker.add_expense(
            "2025-03-01",
            "Food",
            "Lunch",
            150
        )

        self.assertEqual(len(self.tracker.get_all()), 1)

    def test_get_all(self):
        add_expense(
            self.conn,
            "2025-03-01",
            "Food",
            "Lunch",
            150
        )

        self.assertEqual(len(get_all(self.conn)), 1)

    def test_category_totals(self):
        add_expense(
            self.conn, "2025-03-01", "Food", "Lunch", 100
        )

        add_expense(
            self.conn, "2025-03-02", "Food", "Dinner", 200
        )

        totals = totals_by_category(self.conn)

        self.assertEqual(totals[0]["total"], 300)

    def test_month_filter(self):
        add_expense(
            self.conn, "2025-03-01", "Food", "Lunch", 100
        )

        add_expense(
            self.conn, "2025-04-01", "Travel", "Bus", 50
        )

        self.assertEqual(
            len(get_all(self.conn, "2025-03")),
            1
        )

    def test_duplicate_import(self):
        csv_path = Path(self.temp.name) / "expenses.csv"

        csv_path.write_text(
            "date,category,description,amount\n"
            "2025-03-01,Food,Lunch,100\n",
            encoding="utf-8"
        )

        first = import_csv(csv_path, self.conn)
        second = import_csv(csv_path, self.conn)

        self.assertEqual(first, (1, 0, 0))
        self.assertEqual(second, (0, 1, 0))

    def test_invalid_amount(self):
        csv_path = Path(self.temp.name) / "bad.csv"

        csv_path.write_text(
            "date,category,description,amount\n"
            "2025-03-01,Food,Lunch,wrong\n",
            encoding="utf-8"
        )

        result = import_csv(csv_path, self.conn)

        self.assertEqual(result, (0, 0, 1))


if __name__ == "__main__":
    unittest.main()
