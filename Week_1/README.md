# PyAnalytics: Local Automation & Data Processing Hub — Week 1

**Internship task:** Task 1 — Read a CSV and Summarise It  
**Language:** Python  
**Project type:** Menu-driven command-line expense tracker

## Project overview

This program reads expense records from `data/expenses.csv` and displays:
- All expense records in aligned columns
- Total spending by category
- The overall amount spent
- The single biggest expense

## Project structure

```text
PyAnalytics_Week1/
├── main.py
├── data/
│   └── expenses.csv
├── screenshots/
│   └── sample_output.png
├── README.md
└── .gitignore
```

## Requirements

- Python 3.8 or newer
- No external Python packages are required. The program uses Python's built-in `csv` module.

## How to run

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

```bash
python main.py
```

On some systems, use `python3 main.py`.

## Menu options

| Option | What it does |
|---|---|
| 1 | Shows all expense records and the overall total |
| 2 | Shows totals grouped by category |
| 3 | Shows the biggest single expense |
| 4 | Exits the program |

## CSV format

The file `data/expenses.csv` contains 20 sample records and these four columns:

- `date`
- `category`
- `description`
- `amount`

The `amount` values are converted to `float` when the CSV is loaded.

## Functions included

- `load_expenses(path)` — reads CSV data using `csv.DictReader`
- `total_spent(expenses)` — calculates the overall total
- `totals_by_category(expenses)` — groups amounts by category using a dictionary
- `biggest_expense(expenses)` — returns the row with the highest amount
- `display_expenses(expenses)` — prints the expense list
- `display_category_totals(expenses)` — prints category totals
- `display_biggest_expense(expenses)` — prints the largest expense
- `main()` — runs the menu using `while` and `input()`

## Sample output screenshot

See [`screenshots/sample_output.png`](screenshots/sample_output.png).

## Week 1 completion checks

- [x] `main.py` contains separate functions for loading, totalling and displaying data.
- [x] `data/expenses.csv` contains 20 sample rows.
- [x] The menu can be run with `python main.py`.
- [x] The README includes run instructions and a sample output screenshot.
- [x] The program has at least four functions and avoids copy-pasted calculation logic.
- [x] Category totals add up to the overall total.

## GitHub upload

Create a new **public** GitHub repository named `PyAnalytics-Week1` (or another name you prefer), then upload the contents of this project folder. Do not upload the ZIP file inside the repository; upload the extracted files and folders.

Suggested repository description:

> A Python command-line expense tracker that reads CSV data and generates spending summaries by category.

## Internship submission reminder

The SkillMe Week 1 guide also asks you to:
1. Push the code to GitHub with this README.
2. Publish a LinkedIn post with a 30–60 second demo video or 2–3 screenshots.
3. Tag the official `@SkillMe` page.
4. Submit the LinkedIn post URL in the SkillMe Student Dashboard.

Only publish the post after you have run and checked the project yourself.
