
from flask import Flask, render_template, request, jsonify

from banking.account import BankAccount, SavingsAccount, CurrentAccount
from banking.transactions import deposit, withdraw, calculate_interest

app = Flask(__name__)

# Demo storage: accounts reset when the server restarts.
accounts = {}


def get_account(account_number):
    return accounts.get(str(account_number))


def get_balance(account):
    return account.get_balance()


def read_request_data():
    return request.get_json(silent=True) or request.form


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"status": "UP"}), 200


@app.route("/version")
def version():
    return jsonify({
        "application": "Bank Management System",
        "version": "2.0"
    }), 200


@app.route("/api/accounts", methods=["POST"])
def create_account():
    data = read_request_data()

    name = str(data.get("name", "")).strip()
    account_type = str(data.get("accountType", "savings")).lower()

    try:
        initial_balance = float(data.get("initialBalance", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid initial balance."}), 400

    if not name:
        return jsonify({"error": "Name is required."}), 400

    if account_type not in ("savings", "current"):
        return jsonify({"error": "Invalid account type."}), 400

    if initial_balance < 0:
        return jsonify({
            "error": "Initial balance cannot be negative."
        }), 400

    try:
        if account_type == "savings":
            account = SavingsAccount(name, initial_balance)
        else:
            account = CurrentAccount(name, initial_balance)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    account_number = str(account.account_number)
    accounts[account_number] = account

    return jsonify({
        "message": "Account created successfully.",
        "accountNumber": account_number,
        "name": account.name,
        "accountType": account_type,
        "balance": get_balance(account)
    }), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = read_request_data()
    account_number = str(data.get("accountNumber", "")).strip()

    account = get_account(account_number)

    if account is None:
        return jsonify({"error": "Account not found."}), 404

    return jsonify({
        "message": "Login successful.",
        "accountNumber": str(account.account_number),
        "name": account.name,
        "balance": get_balance(account),
        "accountType": (
            "savings" if isinstance(account, SavingsAccount) else "current"
        )
    }), 200


@app.route("/api/accounts/<account_number>", methods=["GET"])
def account_details(account_number):
    account = get_account(account_number)

    if account is None:
        return jsonify({"error": "Account not found."}), 404

    return jsonify({
        "accountNumber": str(account.account_number),
        "name": account.name,
        "balance": get_balance(account)
    }), 200


@app.route("/api/accounts/<account_number>/deposit", methods=["POST"])
def deposit_money(account_number):
    account = get_account(account_number)

    if account is None:
        return jsonify({"error": "Account not found."}), 404

    data = read_request_data()

    try:
        amount = float(data.get("amount", 0))
        deposit(account, amount)
    except (TypeError, ValueError) as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({
        "message": "Deposit successful.",
        "balance": get_balance(account)
    }), 200


@app.route("/api/accounts/<account_number>/withdraw", methods=["POST"])
def withdraw_money(account_number):
    account = get_account(account_number)

    if account is None:
        return jsonify({"error": "Account not found."}), 404

    data = read_request_data()

    try:
        amount = float(data.get("amount", 0))
        withdraw(account, amount)
    except (TypeError, ValueError) as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({
        "message": "Withdrawal successful.",
        "balance": get_balance(account)
    }), 200


@app.route("/api/accounts/<account_number>/interest", methods=["GET"])
def account_interest(account_number):
    account = get_account(account_number)

    if account is None:
        return jsonify({"error": "Account not found."}), 404

    try:
        interest = calculate_interest(account)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify({
        "message": "Interest calculated successfully.",
        "balance": get_balance(account),
        "interestRate": account.interest_rate,
        "interestAdded": round(interest, 2)
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
