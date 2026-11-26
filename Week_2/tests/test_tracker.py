"""Automated checks for the Week 2 tracker."""

import csv
import json
import tempfile
import unittest
from pathlib import Path

from tracker import Expense, ExpenseTracker
from storage import load_expenses, append_expense, export_report_json


class ExpenseTrackerTests(unittest.TestCase):
    def test_category_normalisation_and_totals(self):
        tracker = ExpenseTracker([
            Expense("2026-11-01", " food ", "Breakfast", 100),
            Expense("2026-11-02", "Food", "Lunch", 50),
        ])
        self.assertEqual(tracker.totals_by_category(), {"Food": 150.0})
        self.assertEqual(tracker.total_spent(), 150.0)

    def test_search_ignores_case(self):
        tracker = ExpenseTracker([
            Expense("2026-11-01", "Food", "Python Book", 100),
            Expense("2026-11-02", "Food", "Lunch", 50),
        ])
        self.assertEqual(len(tracker.search("pYtHoN")), 1)

    def test_biggest_expense(self):
        tracker = ExpenseTracker([
            Expense("2026-11-01", "Food", "Tea", 10),
            Expense("2026-11-02", "Shopping", "Bag", 100),
        ])
        self.assertEqual(tracker.biggest_expense().description, "Bag")

    def test_loader_skips_invalid_rows_and_cleans_spaces(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "expenses.csv"
            path.write_text(
                "date,category,description,amount\n"
                "2026-11-01,  Food  , Tea ,10\n"
                "2026-11-02,Food,Missing amount,\n"
                "2026-11-03,Food,Bad amount,abc\n"
                ",,,\n",
                encoding="utf-8",
            )
            expenses, skipped = load_expenses(path)
            self.assertEqual(len(expenses), 1)
            self.assertEqual(skipped, 3)
            self.assertEqual(expenses[0].category, "Food")
            self.assertEqual(expenses[0].description, "Tea")

    def test_added_expense_is_persisted(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "expenses.csv"
            expense = Expense("2026-11-26", "Travel", "Train", 75)
            append_expense(path, expense)
            loaded, skipped = load_expenses(path)
            self.assertEqual(skipped, 0)
            self.assertEqual(len(loaded), 1)
            self.assertEqual(loaded[0].description, "Train")

    def test_json_report(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "report.json"
            tracker = ExpenseTracker([
                Expense("2026-11-01", "Food", "Breakfast", 100),
                Expense("2026-11-02", "Food", "Lunch", 50),
            ])
            export_report_json(path, tracker)
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["overall_total"], 150.0)
            self.assertEqual(data["category_totals"]["Food"], 150.0)


if __name__ == "__main__":
    unittest.main()
