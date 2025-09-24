import datetime

class Transaction:
    def __init__(self, account_id, transaction_type, amount, account_type, status="SUCCESS"):
        self.account_id = account_id
        self.transaction_type = transaction_type  
        self.amount = amount
        self.account_type = account_type 
        self.timestamp = datetime.datetime.now()
        self.status = status