import datetime
class Transaction:
    def __init__(self, amount, narration, transaction_type):
        self.amount = amount
        self.narration = narration
        self.transaction_type = transaction_type
        self.date_time = datetime.datetime.now()
    def __str__(self):
        return f"{self.date_time} - {self.transaction_type.upper()}: {self.narration} | Amount: {self.amount}"
class Account:
    def __init__(self, name, account_number):
        self.name = name
        self.__balance = 0
        self.__account_number = account_number
        self.__transactions = []
        self.loan = 0
        self.loan_status = "inactive"
        self.is_frozen = False
        self.minimum_balance = 100
        self.closed = False
        self.deposit_count = 0
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            self.__transactions.append(Transaction(amount, "Deposit", "deposit"))
            self.deposit_count += 1
            return f"You have successfully deposited{amount}. New balance is {self.__balance}"
        return "Deposit amount must be greater than 0"
    def withdraw(self, amount):
        fee = amount * 0.02
        total_deduction = amount + fee
        if self.is_frozen:
            return "Withdrawal failed: Account is frozen"
        if total_deduction > self.__balance:
            return "Insufficient balance for withdrawal and fee"
        if self.__balance - total_deduction < self.minimum_balance:
            return f"Withdrawal would breach minimum balance of {self.minimum_balance}"
        self.__balance -= total_deduction
        self.__transactions.append(Transaction(amount, "Cash withdrawal", "withdrawal"))
        self.__transactions.append(Transaction(fee, "Withdrawal fee", "fee"))
        return f"Withdrawn {amount} with fee {fee}. New balance is {self.__balance}"
    def get_balance(self):
        return self.__balance
    def get_account_number(self):
        return self.__account_number
    def get_transactions(self):
        return self.__transactions
    def transfer_funds(self, recipient, amount):
        transfer_fee = 10
        total = amount + transfer_fee
        if self.is_frozen:
            return "Transfer denied: Account is frozen"
        if total > self.__balance:
            return "Transfer failed due to insufficient balance (including transfer fee)"
        self.__balance -= total
        recipient.deposit(amount)
        self.__transactions.append(Transaction(amount, f"Transfer to {recipient.name}", "transfer"))
        self.__transactions.append(Transaction(transfer_fee, "Transfer fee", "fee"))
        return f"Transferred {amount} to {recipient.name}. Fee {transfer_fee}. New balance is {self.__balance}"
    def request_loan(self, amount):
        if self.loan_status != "inactive":
            return "You already have a pending loan"
        if self.deposit_count < 2:
            return "Loan denied: Minimum of 2 deposits required"
        if self.__balance < 2000:
            return "Loan denied: Minimum balance of 2000 required"
        self.loan = amount
        self.loan_status = "active"
        self.deposit(amount)
        self.__transactions.append(Transaction(amount, "Loan received and successfully deposited", "loan"))
        return f"Loan received. Amount: {amount}. New balance is {self.__balance}"
    def repay_loan(self, amount):
        if amount <= 0:
            return "Insufficient amount "
        if self.__balance < amount:
            return "Insufficient balance  to pay the loan"
        repay_amount = min(amount, self.loan)
        self.__balance -= repay_amount
        self.loan -= repay_amount
        self.__transactions.append(Transaction(repay_amount, "Loan repayment", "repayment"))
        if self.loan <= 0:
            self.loan = 0
            self.loan_status = "inactive"
        return f"Repaid {repay_amount}. unpaid loan: {self.loan}"
    def change_account_ownership(self, new_owner):
        self.name = new_owner
        return f"Account ownership changed to {new_owner}"
    def apply_interest(self):
        if self.__balance <= 0:
            return "No interest gained on zero or non-positive balance"
        interest = self.__balance * 0.05
        self.__balance += interest
        self.__transactions.append(Transaction(interest, "Interest Added", "interest"))
        return f"Interest of {interest} added. New balance is {self.__balance}"
    def freeze_account(self):
        if not self.is_frozen:
            self.is_frozen = True
            return "Account is frozen"
        return "Account is now frozen"
    def unfreeze_account(self):
        if self.is_frozen:
            self.is_frozen = False
            return f"Account {self.__account_number} has been unfrozen"
        return f"Account {self.__account_number} is not frozen"
    def account_statement(self):
        print(f"Statement for account: {self.__account_number} - {self.name}")
        for transaction in self.__transactions:
            print(transaction)
    def set_minimum_balance(self, amount):
        if amount >= 0:
            self.minimum_balance = amount
            return f"Minimum balance set to {amount}"
        return "Minimum balance must be positive"
    def close_account(self):
        self.__transactions.clear()
        self.__balance = 0
        self.loan = 0
        self.loan_status = "None"
        self.closed = True
        return "Account closed and all funds are  cleared"