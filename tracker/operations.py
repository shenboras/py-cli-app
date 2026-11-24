from datetime import datetime
from tracker.exceptions import ValidationError

ALLOWED_CATEGORIES = ["food", "transport", "utilities", "work", "entertainment", "other"]


def validate_amount(amount: float) -> float:
    if amount <= 0:
        raise ValidationError("amount must be higher than 0.")
    return round(amount, 2)


def validate_category(category: str) -> str:
    clean_category = category.strip().lower()
    if clean_category not in ALLOWED_CATEGORIES:
        categories_text = ", ".join(ALLOWED_CATEGORIES)
        raise ValidationError(f"invalid category: '{category}'. Choose one of: {categories_text}")
    return clean_category


def validate_date(date_text: str | None) -> str:
    if date_text is None:
        return datetime.now().strftime("%Y-%m-%d")

    try:
        parsed_date = datetime.strptime(date_text.strip(), "%Y-%m-%d")
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        raise ValidationError("The format of date must be like YYYY-AA-GG. (eg.: 2026-11-23).")


def add_expense(
                expenses: list[dict], 
                amount: float, 
                category: str, 
                description: str = "", 
                date_text: str | None = None,
                ) -> dict:
                
    clean_amount = validate_amount(amount)
    clean_category = validate_category(category)
    clean_date = validate_date(date_text)
    clean_description = description.strip()

    if expenses:
        next_id = max(item["id"] for item in expenses) + 1
    else:
        next_id = 1

    new_expense = {
        "id": next_id,
        "amount": clean_amount,
        "category": clean_category,
        "description": clean_description,
        "date": clean_date,
    }

    expenses.append(new_expense)
    return new_expense

def get_summary(expenses, category=None):
    filtered_expenses = expenses

    if category is not None:
        clean_category = validate_category(category)
        filtered_expenses = [item for item in expenses if item["category"] == clean_category]

    total = 0.0
    by_category = {}

    for item in filtered_expenses:
        amount = item["amount"]
        cat = item["category"]
        total += amount
        by_category[cat] = by_category.get(cat, 0.0) + amount

    return {
        "count": len(filtered_expenses),
        "total": round(total, 2),
        "by_category": {k: round(v, 2) for k, v in by_category.items()},
    }

def delete_expense(expenses, expense_id):
    for index, item in enumerate(expenses)
        if item["id"] == expense_id:
            return expenses.pop(index)

    raise ValidationError(f"Expense with ID {expense_id} not found.")