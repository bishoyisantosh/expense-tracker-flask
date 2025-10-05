from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    expenses = load_data()

    if request.method == "POST":
        category = request.form["category"]
        amount = float(request.form["amount"])
        expenses.append({"category": category, "amount": amount})
        save_data(expenses)
        return redirect("/")

    total = sum(item["amount"] for item in expenses)
    return render_template("index.html", expenses=expenses, total=total)

@app.route("/delete/<int:index>")
def delete(index):
    expenses = load_data()
    if 0 <= index < len(expenses):
        expenses.pop(index)
        save_data(expenses)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
