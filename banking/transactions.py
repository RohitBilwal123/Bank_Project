
from banking.account import BankAccount


def deposit(account: BankAccount, amount: float):
    """Deposit money into a bank account."""
    return account.deposit(amount)


def withdraw(account: BankAccount, amount: float):
    """Withdraw money from a bank account."""
    return account.withdraw(amount)


def get_balance(account: BankAccount):
    """Get the current balance of an account."""
    return account.get_balance()


def calculate_interest(account: BankAccount):
    """Calculate interest if the account supports it."""
    if not hasattr(account, "calculate_interest"):
        raise ValueError(
            "Interest calculation is available only for savings accounts."
        )

    return account.calculate_interest()
