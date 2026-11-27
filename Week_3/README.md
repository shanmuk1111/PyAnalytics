# PyAnalytics: Local Automation & Data Processing Hub — Week 2

**Internship task:** Week 2 — Classes, Modules and Clean Data  
**Language:** Python 3  
**Project:** Menu-driven command-line expense tracker

## Week 2 overview

This project continues the Week 1 expense tracker. It reorganises the program into classes and modules, cleans messy CSV data, allows new expenses to be saved, supports case-insensitive searching, and exports category totals to JSON.

## Project structure

```text
PyAnalytics_Week2/
├── main.py
├── tracker.py
├── storage.py
├── data/
│   └── expenses.csv
├── report.json              # created when option 6 is selected
├── tests/
│   └── test_tracker.py
├── screenshots/
│   └── sample_output.txt
├── README.md
└── .gitignore
```

## Requirements

- Python 3.8 or newer
- No third-party packages are required.

## How to run

Open a terminal in the project folder and run:

```bash
python main.py
```

The program uses paths relative to `main.py`, so it can also be launched while your terminal is in another folder.

## Menu options

| Option | Feature |
|---|---|
| 1 | Show all valid expenses and overall total |
| 2 | Show totals grouped by category |
| 3 | Show the biggest expense |
| 4 | Add an expense and append it to the CSV |
| 5 | Search descriptions without case sensitivity |
| 6 | Export category totals and overall total to `report.json` |
| 7 | Quit |

## Modules and classes

### `tracker.py`

- `Expense`: stores `date`, `category`, `description`, and `amount`; formats itself with `__str__`.
- `ExpenseTracker`: stores Expense objects and provides `add_expense`, `total_spent`, `totals_by_category`, `biggest_expense`, and `search`.

### `storage.py`

- `load_expenses(path)`: reads CSV data using `csv.DictReader`, trims spaces, normalises categories, and skips blank or invalid rows. Returns both the valid expenses and the skipped-row count.
- `append_expense(path, expense)`: saves a new expense to the CSV.
- `export_report_json(path, tracker)`: writes the category totals and overall total using `json`.

### `main.py`

Contains the command-line menu and user input/display flow. Calculation and file-handling logic live in the other modules.

## Messy CSV data

The sample CSV intentionally includes:
- A category and description with extra spaces (cleaned when loaded).
- A row with a missing amount (skipped).
- A row with `abc` as the amount (skipped).
- A blank row (skipped).

The application prints the number of valid and skipped rows at startup. Invalid rows do not crash the program.

## Run automated tests

From the project folder:

```bash
python -m unittest discover -s tests -v
```

## GitHub: continue your Week 1 repository

This is a Week 2 update to the same PyAnalytics repository. Do not create a separate Week 2 repository if Week 1 is already in your GitHub repository.

1. Extract this ZIP.
2. Copy the contents of this folder into your existing Week 1 repository folder, replacing the old `main.py`, `README.md`, and adding `tracker.py`, `storage.py`, `tests/` and the updated `data/expenses.csv`.
3. Keep the existing `.git` folder in your Week 1 repository. Do not delete it.
4. Open PowerShell inside that existing repository folder and run:

```powershell
git status
git add .
git commit -m "Complete Week 2 classes modules and data cleaning"
git push
```

If Git says there is nothing to commit, check that you copied the Week 2 files into the correct repository folder. If `git push` reports that no upstream branch is configured, run:

```powershell
git push -u origin main
```

Do not run `git init` or `git remote add origin` again when continuing the existing repository.

## Week 2 completion checklist

- [x] `Expense` class with `__init__` and `__str__`.
- [x] `ExpenseTracker` class with Week 1 calculations moved into methods.
- [x] Classes in `tracker.py`; file operations in `storage.py`; menu in `main.py`.
- [x] Messy CSV rows are cleaned or skipped and counted.
- [x] Add expense validates the amount and persists the new row.
- [x] Search is case-insensitive.
- [x] JSON report contains category totals and overall total.
- [x] Week 1 features remain available.
- [x] Automated tests included.

## LinkedIn submission

After running the program and capturing 2–3 screenshots or a 30–60 second demo, publish a post tagging **@SkillMe**. Put the GitHub repository link in the post or its first comment, then submit the LinkedIn post URL on the SkillMe dashboard.
