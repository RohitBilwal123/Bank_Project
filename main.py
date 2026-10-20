
from banking.account import Account
from banking.transactions import deposit, withdraw


accounts = {}
next_account_number = 100001


def create_account():
    """Create a new bank account."""
    global next_account_number

    print("\n===== CREATE ACCOUNT =====")

    name = input("Enter your name: ").strip()

    if not name:
        print("Error: Name cannot be empty.")
        return

    print("1. Savings Account")
    print("2. Current Account")

    account_type = input("Select account type: ").strip()

    if account_type not in ("1", "2"):
        print("Invalid account type.")
        return

    try:
        initial_balance = float(input("Enter initial balance: ₹"))

        if initial_balance < 0:
            print("Initial balance cannot be negative.")
            return

    except ValueError:
        print("Please enter a valid amount.")
        return

    try:
        account = Account(name, initial_balance)
    except TypeError:
        account = Account(name)

        if hasattr(account, "balance"):
            account.balance = initial_balance

    account_number = str(next_account_number)
    next_account_number += 1

    accounts[account_number] = {
        "account": account,
        "name": name,
        "type": "Savings" if account_type == "1" else "Current"
    }

    print("\nAccount created successfully!")
    print(f"Account Number: {account_number}")
    print(f"Account Holder: {name}")
    print(f"Account Type: {accounts[account_number]['type']}")
    print(f"Initial Balance: ₹{get_balance(account):.2f}")


def get_balance(account):
    """Return the account balance."""
    if hasattr(account, "balance"):
        return float(account.balance)

    if hasattr(account, "get_balance"):
        return float(account.get_balance())

    return 0.0


def login():
    """Log in using an account number."""
    print("\n===== ACCOUNT LOGIN =====")

    account_number = input("Enter account number: ").strip()

    account_data = accounts.get(account_number)

    if account_data is None:
        print("Account not found. Please create an account first.")
        return

    account_menu(account_number, account_data)


def account_menu(account_number, account_data):
    """Display banking operations for the selected account."""
    account = account_data["account"]

    while True:
        print("\n===== BANK ACCOUNT MENU =====")
        print(f"Welcome, {account_data['name']}!")
        print(f"Account Number: {account_number}")
        print(f"Balance: ₹{get_balance(account):.2f}")

        print("\n1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. Calculate Interest")
        print("5. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            deposit_money(account)

        elif choice == "2":
            withdraw_money(account)

        elif choice == "3":
            print(f"Current Balance: ₹{get_balance(account):.2f}")

        elif choice == "4":
            calculate_interest(account)

        elif choice == "5":
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice. Please try again.")


def deposit_money(account):
    """Deposit money into an account."""
    try:
        amount = float(input("Enter deposit amount: ₹"))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        result = deposit(account, amount)

        if result is False:
            print("Deposit failed.")
        else:
            print("Deposit completed successfully.")
            print(f"Updated Balance: ₹{get_balance(account):.2f}")

    except ValueError:
        print("Please enter a valid amount.")


def withdraw_money(account):
    """Withdraw money from an account."""
    try:
        amount = float(input("Enter withdrawal amount: ₹"))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        if amount > get_balance(account):
            print("Insufficient balance.")
            return

        result = withdraw(account, amount)

        if result is False:
            print("Withdrawal failed.")
        else:
            print("Withdrawal completed successfully.")
            print(f"Updated Balance: ₹{get_balance(account):.2f}")

    except ValueError:
        print("Please enter a valid amount.")


def calculate_interest(account):
    """Calculate estimated annual interest at 4%."""
    balance = get_balance(account)
    interest_rate = 0.04
    interest = balance * interest_rate

    print("\n===== INTEREST DETAILS =====")
    print("Annual Interest Rate: 4%")
    print(f"Current Balance: ₹{balance:.2f}")
    print(f"Estimated Annual Interest: ₹{interest:.2f}")


def main():
    """Main application menu."""
    while True:
        print("\n================================")
        print("    BANK MANAGEMENT SYSTEM")
        print("================================")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_account()

        elif choice == "2":
            login()

        elif choice == "3":
            print("Thank you for using our banking system!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
