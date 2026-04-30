from flask import Flask, render_template, jsonify
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_loader import get_transactions
from modules.categories import group_by_category, get_top_categories, format_categories
from modules.cashback import get_top_cashback_categories
from modules.search import search_transactions

app = Flask(__name__)

# Загружаем данные один раз
transactions = get_transactions()

# Бизнес-логика
expenses = group_by_category(transactions)
top_categories = get_top_categories(expenses)
formatted_categories = format_categories(top_categories)
top_cashback = get_top_cashback_categories(transactions)

# Итоги
total_expenses = sum(abs(t["amount"]) for t in transactions if t["amount"] < 0)
total_incomes = sum(t["amount"] for t in transactions if t["amount"] > 0)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/summary")
def api_summary():
    return jsonify(
        {
            "total_transactions": len(transactions),
            "total_expenses": round(total_expenses),
            "total_incomes": round(total_incomes),
            "balance": round(total_incomes - total_expenses),
        }
    )


@app.route("/api/categories")
def api_categories():
    return jsonify(formatted_categories)


@app.route("/api/cashback")
def api_cashback():
    return jsonify(top_cashback)


@app.route("/api/search/<query>")
def api_search(query):
    results = search_transactions(transactions, query)
    return jsonify(results[:50])


if __name__ == "__main__":
    app.run(debug=True)
