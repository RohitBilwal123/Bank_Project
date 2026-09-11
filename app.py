from flask import Flask, render_template, request, jsonify
from banking.account import SavingsAccount, CurrentAccount

app = Flask(__name__)

accounts = {}


@app.route("/")
def home():
    return render_template("index.html")


# CREATE ACCOUNT
@app.route("/create-account", methods=["POST"])
def create_account():
    data = request.get_json()

    name = data.get("name")
    account_type = data.get("account_type")
    balance = float(data.get("balance", 0))

    if account_type == "savings":
        account = SavingsAccount(name, balance)

    elif account_type == "current":
        account = CurrentAccount(name, balance)

    else:
        return jsonify({"error": "Invalid account type"}), 400

    accounts[account.account_number] = account

    return jsonify({
        "message": "Account created successfully",
        "account_number": account.account_number,
        "name": account.name,
        "balance": account.get_balance()
    })


# LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    account_number = int(data.get("account_number"))

    if account_number not in accounts:
        return jsonify({"error": "Account not found"}), 404

    account = accounts[account_number]

    return jsonify({
        "message": f"Welcome, {account.name}",
        "account_number": account.account_number,
        "name": account.name,
        "balance": account.get_balance()
    })


# DEPOSIT
@app.route("/deposit", methods=["POST"])
def deposit():
    data = request.get_json()

    account_number = int(data.get("account_number"))
    amount = float(data.get("amount"))

    if account_number not in accounts:
        return jsonify({"error": "Account not found"}), 404

    account = accounts[account_number]
    account.deposit(amount)

    return jsonify({
        "message": "Deposit successful",
        "balance": account.get_balance()
    })


# WITHDRAW
@app.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.get_json()

    account_number = int(data.get("account_number"))
    amount = float(data.get("amount"))

    if account_number not in accounts:
        return jsonify({"error": "Account not found"}), 404

    account = accounts[account_number]
    account.withdraw(amount)

    return jsonify({
        "message": "Withdrawal successful",
        "balance": account.get_balance()
    })


# CHECK BALANCE
@app.route("/balance/<int:account_number>", methods=["GET"])
def balance(account_number):

    if account_number not in accounts:
        return jsonify({"error": "Account not found"}), 404

    account = accounts[account_number]

    return jsonify({
        "account_number": account.account_number,
        "name": account.name,
        "balance": account.get_balance()
    })


# CALCULATE INTEREST
@app.route("/interest/<int:account_number>", methods=["GET"])
def interest(account_number):

    if account_number not in accounts:
        return jsonify({"error": "Account not found"}), 404

    account = accounts[account_number]

    if hasattr(account, "calculate_interest"):
        interest_amount = account.calculate_interest()

        return jsonify({
            "message": "Interest calculated",
            "interest": interest_amount,
            "balance": account.get_balance()
        })

    return jsonify({
        "error": "Interest is only available for Savings Account"
    }), 400


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )