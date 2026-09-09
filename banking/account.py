class BankAccount:
    
    account_counter = 1000 #class variable
    def __init__(self, name, balance=0):
        self.name = name
        self.__balance = balance
        self.account_number = BankAccount.account_counter
        BankAccount.account_counter += 1 #increment the class variable
    
    def get_balance(self):
        return self.__balance
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited {amount}. New balance is {self.__balance}.")
        else:
            print("Deposit amount must be greater than 0.") 
    
    def withdraw(self, amount):
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount
            print(f"Withdrew {amount}. New balance is {self.__balance}.")
        else:
            print("Withdrawal amount must be greater than 0 and less than or equal to the balance.")
            
    def display_account_info(self):
        print(f"Account Number: {self.account_number}, Account Holder: {self.name}, Balance: {self.__balance}")


class SavingsAccount(BankAccount):
    
    def __init__(self, name, balance=0, interest_rate=0.02):
        super().__init__(name, balance)
        self.interest_rate = interest_rate
    
    def calculate_interest(self):
        interest = self.get_balance() * self.interest_rate
        self.deposit(interest)
        print(f"Applied interest of {interest}. New balance is {self.get_balance()}.")
        
class CurrentAccount(BankAccount):
    def __init__(self, name, balance=0, overdraft_limit=5000):
        super().__init__(name, balance)
        self.overdraft_limit = overdraft_limit
        