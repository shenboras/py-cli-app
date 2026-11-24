import argparse
import sys
from tracker.exceptions import ExpenseTrackerError
from tracker.operations import add_expense, delete_expense, get_summary
from tracker.storage import load_expenses , save_expenses

DATA_FILE = "data/expenses.json"

def create_parser():
    parser = argparse.ArgumentParser(description="Simple Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command",required=True)

    #add command
    add_cmd = subparsers.add_parser("add", help="Add a new expense")
    add_cmd.add_argument("amount", type=float, help="Expense Amount")
    add_cmd.add_argument("category", type=str, help="Expense Category")
    add_cmd.add_argument("-d", "--description", type=str, default="", help="optional note")
    add_cmd.add_argument("--date", type=str, default=None, help="Date (YYYY-MM-DD)")

    #list command
    list_cmd = subparsers.add_parser("list", help="List expenses")
    list_cmd.add_argument("-c", "--category", type=str, default=None, help="filter by category")

    #summary command
    summary_cmd = subparsers.add_parser("summary", help="SHow Expense Summary")
    summary_cmd.add_argument("-c", "--category", type=str, default=None, help="Filter by category")

    #delete command
    delete_cmd = subparsers.add_parser("delete", help="Delete an expense by ID")
    delete_cmd.add_argument("id", type=int, help="Expense ID")

    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()

    try:
        expenses = load_expenses(DATA_FILE)

        if args.command == "add":
            item = add_expense(
                expenses=expenses,
                amount=args.amount,
                category=args.category,
                descriptuon=args.description,
                date_text=args.date,
            )
            save_expenses(DATA_FILE, expenses)
            print(f"Added -> #{item['id']} | {item['date']} | {item['category']} | {item['amount']:.2f}")

        elif args.command == "list":
            items = expenses
            if args.category is not None:
                clean_cat = args.category.strip().lower()
                items = [e for e in expenses if e["category"] == clean_cat]

            if not items:
                print("No expenses found.")
                return

            for e in items:
                desc_part = f" ({e['description']})" if e["description"] else ""
                print(f"@{e['id']} | {e['date']} | {e['category']} | {e['amount']:.2f}{desc_part}")

        elif args.command == "summary":
            summary = get_summary(expenses, category=args.category)
            print(f"Total Records: {summary['count']} | Grand Total: {summary['total']:.2f}")
            for cat, total in summary["by_category"].items():
                print(f"  - {cat}: {total:.2f}")

        elif args.command == "delete":
            removed = delete_expense(expenses, args.id)
            save_expenses(DATA_FILE, expenses)
            print(f"Deleted -> #{removed['id']} ({removed['amount']:.2f})")

    
    except ExpenseTrackerError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        print(f"Unexpected error: {err}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()