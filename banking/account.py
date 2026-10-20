
class BankAccount:
    """Base class for bank accounts."""

    account_counter = 1000

    def __init__(self, name, balance=0):
        if not name or not name.strip():
            raise ValueError("Account holder name cannot be empty.")

        if balance < 0:
            raise ValueError("Initial balance cannot be negative.")

        self.name = name.strip()
        self.__balance = float(balance)
        self.account_number = BankAccount.account_counter
        BankAccount.account_counter += 1

    def get_balance(self):
        """Return the current account balance."""
        return self.__balance

    def deposit(self, amount):
        """Deposit a positive amount."""
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")

        self.__balance += amount
        return self.__balance

    def withdraw(self, amount):
        """Withdraw money if sufficient funds are available."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")

        if amount > self.__balance:
            raise ValueError("Insufficient balance.")

        self.__balance -= amount
        return self.__balance

    def display_account_info(self):
        """Return account details."""
        return {
            "account_number": self.account_number,
            "name": self.name,
            "balance": self.get_balance()
        }


class SavingsAccount(BankAccount):
    """Savings account with interest calculation."""

    def __init__(self, name, balance=0, interest_rate=0.02):
        super().__init__(name, balance)
        self.interest_rate = interest_rate

    def calculate_interest(self):
        """Calculate and apply interest to the balance."""
        interest = self.get_balance() * self.interest_rate
        self.deposit(interest)
        return interest


class CurrentAccount(BankAccount):
    """Current account with an overdraft limit."""

    def __init__(self, name, balance=0, overdraft_limit=5000):
        super().__init__(name, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        """Allow withdrawals up to the configured overdraft limit."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")

        if amount > self.get_balance() + self.overdraft_limit:
            raise ValueError("Overdraft limit exceeded.")

        # Use the base class's balance update logic.
        if amount <= self.get_balance():
            return super().withdraw(amount)

        overdraft_used = amount - self.get_balance()
        self._BankAccount__balance -= amount
        return self.get_balance()
