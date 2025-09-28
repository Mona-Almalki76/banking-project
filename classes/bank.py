from classes.customer import Customer
import csv
import os
from classes.transaction import Transaction

class Bank:
    def __init__(self):
        self.customers = {}
        self.logged_in_customer = None
        self.transactions = []

    # generate account id automatically
    def auto_id_generated(self):
        if self.customers:
            max_id = 0
            for account_id in self.customers.keys():
                account_num = int(account_id)
                if account_num > max_id:
                    max_id = account_num
            return str(max_id + 1)
        return "10001" # no customer yet

    # Add New Customer
    def add_customer(self, frst_name, last_name, password, given_id=None, create_checking=True, create_savings=True):
        # cashiers can type in an id or this can be automatically generated
        if given_id:
            account_id = given_id
        else:
            account_id = self.auto_id_generated()

        # customer can have a checking account
        # customer can have a savings account
        # customer can have both a checking and a savings account
        if create_checking:
            balance_checking = 0.0
        else:
            balance_checking = None

        if create_savings:
            balance_savings = 0.0
        else:
            balance_savings = None

        customer = Customer(account_id, frst_name, last_name, password, balance_checking, balance_savings)
        self.customers[account_id] = customer
        return customer
    
    # load customers
    def load_customers_from_csv(self, filename="bank.csv"):
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                customer = Customer(
                    row["account_id"],
                    row["frst_name"],
                    row["last_name"],
                    row["password"],
                    float(row["balance_checking"]) if row["balance_checking"] else None,
                    float(row["balance_savings"]) if row["balance_savings"] else None
                )
                self.customers[customer.account_id] = customer

    
    # login
    def login(self, account_id, password):
        customer = self.customers.get(account_id)
        if not customer:
            raise ValueError("Account not found")
        if customer.password != password:
            raise PermissionError("Invalid password")
        self.logged_in_customer = customer
        return True

    # logout
    def logout(self):
        self.logged_in_customer = None

    # save customers to csv file
    def save_customers_to_csv(self, filename="bank.csv"):
        fieldnames = ["account_id", "frst_name", "last_name",
                    "password", "balance_checking", "balance_savings"]
        
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()

            for customer in self.customers.values():
                writer.writerow({
                    "account_id": customer.account_id,
                    "frst_name": customer.frst_name,
                    "last_name": customer.last_name,
                    "password": customer.password,
                    "balance_checking": customer.balance_checking,
                    "balance_savings": customer.balance_savings
                })
    
    # withdraw money from Account
    def withdraw(self, amount, account_type="checking"):
        if not self.logged_in_customer:
            raise PermissionError("Login required to perform withdrawal")

        try:
            if account_type == "checking":
                self.logged_in_customer.withdraw_checking(amount)
            elif account_type == "savings":
                self.logged_in_customer.withdraw_savings(amount)
            else:
                raise ValueError("Invalid account type")

            transaction = Transaction(
                self.logged_in_customer.account_id,
                "withdraw",
                amount,
                account_type
            )
            self.transactions.append(transaction)

            self.save_customers_to_csv()

            self.save_transactions_to_csv()

            return transaction

        except ValueError as e:
            transaction = Transaction(
                self.logged_in_customer.account_id,
                "withdraw",
                amount,
                account_type,
                status="FAILED"
            )
            self.transactions.append(transaction)
            self.save_transactions_to_csv()
            raise e
    
    # deposit money into Account
    def deposit(self, amount, account_type="checking"):
        if not self.logged_in_customer:
            raise PermissionError("Login required to perform deposit")

        try:
            if account_type == "checking":
                self.logged_in_customer.deposit_checking(amount)
            elif account_type == "savings":
                self.logged_in_customer.deposit_savings(amount)
            else:
                raise ValueError("Invalid account type")

            transaction = Transaction(
                self.logged_in_customer.account_id,
                "deposit",
                amount,
                account_type
            )
            self.transactions.append(transaction)

            self.save_customers_to_csv()

            self.save_transactions_to_csv()

            return transaction

        except ValueError as e:
            transaction = Transaction(
                self.logged_in_customer.account_id,
                "deposit",
                amount,
                account_type,
                status="FAILED"
            )
            self.transactions.append(transaction)
            self.save_transactions_to_csv()
            raise e

    # transfer money between accounts of the same customer
    def transfer(self, amount, from_account, to_account, recipient_account_id=None):
        if not self.logged_in_customer:
            raise PermissionError("Login required to perform transfer")

        sender_customer = self.logged_in_customer
        recipient_customer = sender_customer

        if recipient_account_id:
            # transfer to another customer
            recipient_customer = self.customers.get(recipient_account_id)
            if not recipient_customer:
                raise ValueError("Recipient account not found") 

        try:
            # withdraw from sender
            if from_account == "checking":
                sender_customer.withdraw_checking(amount)
            elif from_account == "savings":
                sender_customer.withdraw_savings(amount)
            else:
                raise ValueError("Invalid sender account type")

            # deposit to recipient
            if to_account == "checking":
                recipient_customer.deposit_checking(amount)
            elif to_account == "savings":
                recipient_customer.deposit_savings(amount)
            else:
                raise ValueError("Invalid recipient account type")
            
            recipient_customer.reactivate_account()

            transaction = Transaction(
                sender_customer.account_id,
                "transfer",
                amount,
                f"{from_account}->{to_account}",
                status="SUCCESS"
            )
            self.transactions.append(transaction)

            self.save_customers_to_csv()

            self.save_transactions_to_csv()
            return transaction

        except ValueError as e:
            transaction = Transaction(
                sender_customer.account_id,
                "transfer",
                amount,
                f"{from_account}->{to_account}",
                status="FAILED"
            )
            self.transactions.append(transaction)
            self.save_transactions_to_csv()

            raise e

    # transactions (csv)
    def save_transactions_to_csv(self, filename="transactions.csv"):
        fieldnames = ["account_id", "transaction_type", "amount", "account_type", "status", "timestamp"]

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for t in self.transactions:
                writer.writerow({
                    "account_id": t.account_id,
                    "transaction_type": t.transaction_type,
                    "amount": t.amount,
                    "account_type": t.account_type,
                    "status": t.status,
                    "timestamp": t.timestamp
                })

    def get_customer_transactions(self, account_id=None, filename="transactions.csv"):
        account_id = account_id or (self.logged_in_customer.account_id if self.logged_in_customer else None)
        if not account_id:
            raise PermissionError("Login required to view transactions")
        
        transactions = []
        try:
            with open(filename, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["account_id"] == account_id:
                        transactions.append(row)
        except FileNotFoundError:
            pass

        return transactions

    def show_transaction_details(self, index, account_id=None, filename="transactions.csv"):
        customer_transactions = self.get_customer_transactions(account_id, filename)
        if index < 0 or index >= len(customer_transactions):
            raise IndexError("Transaction index out of range")
        t = customer_transactions[index]
        return {
            "account_id": t["account_id"],
            "type": t["transaction_type"],
            "amount": t["amount"],
            "account_type": t["account_type"],
            "status": t["status"],
            "timestamp": t["timestamp"]
        }


