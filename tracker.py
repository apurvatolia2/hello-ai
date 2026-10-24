import argparse
import json
import os

FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.json")


def load():
    if os.path.exists(FILE):
        with open(FILE, encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return data
            except json.JSONDecodeError:
                return []
    return []


def save(expenses):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2)


def add(amount, category):
    expenses = load()
    expenses.append({"amount": amount, "category": category})
    save(expenses)
    print(f"Added: {amount} for {category}")


def list_expenses():
    expenses = load()
    for e in expenses:
        print(f"{e['amount']} - {e['category']}")


def total():
    expenses = load()
    total_amount = sum(float(e["amount"]) for e in expenses)
    print(f"Total: {total_amount:.2f}")


def summary():
    expenses = load()
    if not expenses:
        print("No expenses recorded.")
        return

    total_amount = sum(float(e["amount"]) for e in expenses)
    category_totals = {}
    for expense in expenses:
        category = expense.get("category", "uncategorized")
        category_totals[category] = category_totals.get(category, 0.0) + float(expense["amount"])

    print(f"Total: {total_amount:.2f}")
    for category, amount in sorted(category_totals.items()):
        print(f"{category}: {amount:.2f}")


parser = argparse.ArgumentParser(description="Track personal expenses.")
sub = parser.add_subparsers(dest="command")

p_add = sub.add_parser("add", help="Add a new expense")
p_add.add_argument("amount", type=float)
p_add.add_argument("category")

sub.add_parser("list", help="List all expenses")
sub.add_parser("total", help="Show the overall total")
sub.add_parser("summary", help="Show the total and per-category breakdown")

args = parser.parse_args()

if args.command == "add":
    add(args.amount, args.category)
elif args.command == "list":
    list_expenses()
elif args.command == "total":
    total()
elif args.command == "summary":
    summary()
else:
    parser.print_help()