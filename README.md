# Expense Tracker CLI

A modular Python CLI application for tracking expenses with input validation, custom exceptions, and JSON persistence.

## Project Structure

```text
expense-tracker-cli/
├── main.py
└── tracker/
    ├── __init__.py
    ├── exceptions.py
    ├── operations.py
    └── storage.py


## Example Usage

python3 main.py add 15.50 food -d "Lunch"
python3 main.py add 4.20 transport --date 2026-11-24
python3 main.py list
python3 main.py list -c food
python3 main.py summary
python3 main.py delete 1