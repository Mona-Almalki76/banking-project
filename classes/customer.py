class Customer:
    def __init__(self,account_id,frst_name,last_name,password,balance_checking,balance_savings):
        self.account_id=account_id
        self.frst_name=frst_name
        self.last_name=last_name
        self.password=password
        self.balance_checking=balance_checking
        self.balance_savings=balance_savings

    def withdraw_checking(self, amount):
        if self.balance_checking is None:
            raise ValueError("No checking account")
        if amount > self.balance_checking:
            raise ValueError("Insufficient funds in checking")
        self.balance_checking -= amount
        return self.balance_checking

    def withdraw_savings(self, amount):
        if self.balance_savings is None:
            raise ValueError("No savings account")
        if amount > self.balance_savings:
            raise ValueError("Insufficient funds in savings")
        self.balance_savings -= amount
        return self.balance_savings
    
    def deposit_checking(self, amount):
        if self.balance_checking is None:
            raise ValueError("No checking account available")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance_checking += amount

    def deposit_savings(self, amount):
        if self.balance_savings is None:
            raise ValueError("No savings account available")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance_savings += amount
