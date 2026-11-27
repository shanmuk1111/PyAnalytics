
import sqlite3
from pathlib import Path

DB_NAME = Path(__file__).resolve().parent / "expenses.db"



def get_connection(db_path=DB_NAME):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            source_key TEXT UNIQUE
        )
    """)

    conn.commit()
    return conn


def add_expense(conn, date, category, description, amount, source_key=None):
    cursor = conn.execute("""
        INSERT OR IGNORE INTO expenses
        (date, category, description, amount, source_key)
        VALUES (?, ?, ?, ?, ?)
    """, (date, category, description, amount, source_key))

    conn.commit()
    return cursor.rowcount == 1


def get_all(conn, month=None):
    if month:
        return conn.execute("""
            SELECT * FROM expenses
            WHERE date LIKE ?
            ORDER BY date
        """, (month + "%",)).fetchall()

    return conn.execute("""
        SELECT * FROM expenses
        ORDER BY date
    """).fetchall()


def totals_by_category(conn, month=None):
    if month:
        return conn.execute("""
            SELECT category, SUM(amount) AS total
            FROM expenses
            WHERE date LIKE ?
            GROUP BY category
            ORDER BY category
        """, (month + "%",)).fetchall()

    return conn.execute("""
        SELECT category, SUM(amount) AS total
        FROM expenses
        GROUP BY category
        ORDER BY category
    """).fetchall()


def delete_expense(conn, expense_id):
    cursor = conn.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )
    conn.commit()
    return cursor.rowcount > 0
