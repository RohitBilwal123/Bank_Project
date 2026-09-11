from banking.account import SavingsAccount, CurrentAccount


def test_savings_account():
    account = SavingsAccount("Rohit", 1000)
    assert account.get_balance() == 1000


def test_deposit():
    account = SavingsAccount("Rohit", 1000)
    account.deposit(500)
    assert account.get_balance() == 1500


def test_withdraw():
    account = SavingsAccount("Rohit", 1000)
    account.withdraw(300)
    assert account.get_balance() == 700


def test_current_account():
    account = CurrentAccount("Rohit", 2000)
    assert account.get_balance() == 2000