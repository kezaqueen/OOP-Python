
class Account:
    def __init__(self,owner,min_balance=0):
        self.owner = owner
        self.deposits = []
        self.withdrawals = []
        self.loan_balance = 0
        self.transactions = []
        self.frozen = False
        self.min_balance = min_balance
        self.closed = False

    def deposit(self,amount):
        if self.closed or self.frozen:
            return "Account is dormant."
        elif amount <= 0:
            return "Deposit amount must not be negative"
        self.deposits.append(amount)
        self.transactions.append(f"Deposited: {amount}")
        return f"Deposited successful. Your new balance: {self.get_balance()}"

    def withdraw(self,amount):
        if self.closed or self.frozen:
            return "Account is dormant"
        elif amount <= 0:
            return "Withdraw amount must not be negative"
        elif self.get_balance()-amount < self.min_balance:
            return "Insufficient balance."
        self.withdrawals.append(amount)
        self.transactions.append(f"Withdrew: {amount}")
        return f"Withdrawal successful. New balance : {self.get_balance()}"

    def transfer(self, recipient_account, amount):
        if  amount <= self.min_balance:
            self.withdraw(amount)
            self.deposit(amount)
            print(f"Transferred ${amount} to account {recipient_account}.")
        else:
            print("Insufficient funds or invalid transfer amount.")

    def get_balance(self):
        return sum(self.deposits) - sum(self.withdrawals) - self.loan_balance

    def request_loan(self,amount):
        if amount <= 0:
            return "Loan amount must be positive"
        self.loan_balance += amount
        self.transactions.append(f"Loan requested : {amount}")
        return f"Loan approved. Loan balance is now {self.loan_balance}"

    def repay_loan (self,amount):
        if amount <= 0:
            return "Paying amount must be positive"
        elif amount >self.loan_balance:
            excess = amount - self.loan_balance
            self.loan_balance = 0
            self.deposits.append(excess)
            self.transactions.append(f"Loan payed: {amount}, Excess deposited: {excess}")
            return f"Loan fully repaid . Excess{excess} added to account."
        else:
            self.loan_balance -= amount 
            self.transactions.append(f" loan repayment : {amount}")
            return f"Loan rapayment successful. Remaining loan balance : {self.loan_balance}"

    def View_account_details(self):
        return f"Account owner: {self.owner},Balance:{self.get_balance()}"

    def change_account_owner(self,new_name):
        self.owner = new_name 
        return f"Account owner changed to {self.owner}"

    def account_statement(self):
        print("Account statement:")
        for entry in self.transactions:
            print(entry)
        print(f"Current Balance: {self.get_balance()}")

    def interest_calculation(self):
        interest = self.get_balance()*0.05
        self.deposits.append(interest)
        self.transactions.append(f"Interest added: {interest}")
        return f"Interest of {interest}applied. New balance is {self.get_balance()}"

    def freeze_account(self):
        self.frozen = True 
        return "Account is frozen"

    def unfreeze_account(self):
        self.frozen = False
        return "Account is unfrozen"

    def set_minimum_balance(self,amount):
        if amount < 0:
            return "Minimum balance must be non-negative"
        self.min_balance = amount
        return f"Minimum balance set to{amount}"

    def close_account (self):
        self.deposits.clear()
        self.withdrawals.clear()
        self.transactions.clear()
        self.loan_balance = 0
        self.closed = True
        return "Account is closed and all funds are cleared"  



